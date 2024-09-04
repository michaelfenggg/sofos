import os
import argparse
import cv2
import numpy as np
import sys
import time
import importlib.util
from tensorflow.lite.python.interpreter import Interpreter
from tensorflow.lite.python.interpreter import load_delegate
# from tflite_runtime.interpreter import Interpreter
# from tflite_runtime.interpreter import load_delegate

'''
Requirements: 
1) Install the tflite_runtime package from here:
https://www.tensorflow.org/lite/guide/python
2) Camera to take inputs
3) [Optional] libedgetpu.so.1.0 installed from here if you want to use the edgetpu:
https://github.com/google-coral/edgetpu/tree/master/libedgetpu/direct

Prepraration:
1) Download label:
$ wget https://raw.githubusercontent.com/google-coral/edgetpu/master/test_data/coco_labels.txt
2) Download models:
$ wget https://github.com/google-coral/edgetpu/raw/master/test_data/mobilenet_ssd_v2_coco_quant_postprocess.tflite
$ wget https://github.com/google-coral/edgetpu/raw/master/test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite

Run:
1) With out edgetpu:
$ python3 tflite_cv.py --model mobilenet_ssd_v2_coco_quant_postprocess.tflite --labels coco_labels.txt

2) With edgetpu:
$ python3 tflite_cv.py --model mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite --labels coco_labels.txt --edgetpu True
'''


def load_label(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        lines = f.readlines()
        if not lines:
            return {}
        if lines[0].split(' ', maxsplit=1)[0].isdigit():
            pairs = [line.split(' ', maxsplit=1) for line in lines]
            return {int(index): label.strip() for index, label in pairs}
        else:
            return {index: line.strip() for index, line in enumerate(lines)}

def get_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='Path to tflite model.', required=True)
    parser.add_argument('--labels', help='Path to label file.', required=True)
    parser.add_argument(
        '--threshold', help='Minimum confidence threshold.', default=0.5)
    parser.add_argument('--source', help='Video source.', default=0)
    parser.add_argument('--edgetpu', help='With EdgeTpu', default=False)
    return parser.parse_args()


def main():

    args = get_cmd()

    if args.edgetpu:
        interpreter = Interpreter(args.model, experimental_delegates=[
                                  load_delegate('libedgetpu.so.1.0')])
    else:
        interpreter = Interpreter(args.model)

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    # print(output_details)
    width = 320
    height = 1200
    # print(width, height)

    labels = load_label(args.labels)

        # Capturing the video.
    cap = cv2.VideoCapture(0)
    image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print(image_width, image_height)

    movement_results = [
        {'label': 'Other hand washing movement', 'count': 0, 'code': 0}, 
        {'label': 'Palm to palm', 'count': 0, 'code': 1}, 
        {'label': 'Palm over dorsum, fingers interlaced', 'count': 0, 'code': 2},
        {'label': 'Palm to palm, fingers interlaced', 'count': 0, 'code': 3},
        {'label': 'Backs of fingers to opposing palm, fingers interlocked', 'count': 0, 'code': 4},
        {'label': 'Rotational rubbing of the thumb', 'count': 0, 'code': 5}, 
        {'label': 'Fingertips to palm', 'count': 0, 'code': 6}, 
    ]
    total_movement_count = 0
    total_frames = 0

    # print(interpreter.get_input_details())

    frame_counter = 0
    start = time.time()
    while(True):
        total_frames += 1
        frame_counter += 1
        # Acquire frame and resize to expected shape [1xHxWx3]
        ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        # print(frame_resized, frame_resized.shape)
        input_data = np.expand_dims(frame_resized.astype('float32'), axis=1)
        # input_data = np.expand_dims(input_data, axis=3)
        input_data = np.reshape(frame_resized.astype('float32'), (-1, 5, 240, 320, 3))
        # print(input_data.shape)
        
        # print(input_data.shape)
        # input_data = np.expand_dims(input_data, axis=3)

        # set frame as input tensors
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # perform inference
        interpreter.invoke()

        # Get output tensor
        # print(output_details)
        scores_raw = interpreter.get_tensor(output_details[0]['index'])
        scores = scores_raw[0]

        # Loop over all detections and record movement if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > args.threshold) and (scores[i] <= 1.0)):
                for d in movement_results:
                    if d["code"] == i:
                        d.update({"label": d["label"], 
                                  "count": (d["count"] + 1), 
                                  "code": d["code"]})
                total_movement_count += 1

        print(movement_results, scores, total_movement_count, total_frames)

        # interpreter.get_tensor(output_details[0])
        # interpreter.get_tensor(output_details)
        # boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        # classes = [1, 2, 3, 4, 5, 6, 7]
        # scores = interpreter.get_tensor(output_details[2]['index'])

        # # Loop over all detections and draw detection box if confidence is above minimum threshold
        # for i in range(len(scores)):
        #     if ((scores[i] > args.threshold) and (scores[i] <= 1.0)):
        #         # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
        #         ymin = int(max(1, (boxes[i][0] * image_height)))
        #         xmin = int(max(1, (boxes[i][1] * image_width)))
        #         ymax = int(min(image_height, (boxes[i][2] * image_height)))
        #         xmax = int(min(image_width, (boxes[i][3] * image_width)))

        #         cv2.rectangle(frame, (xmin, ymin),
        #                       (xmax, ymax), (10, 255, 0), 4)

        #                         # Draw label
        #         object_name = labels[int(classes[i])]
        #         label = '%s: %d%%' % (object_name, int(scores[i]*100))
        #         labelSize, baseLine = cv2.getTextSize(
        #             label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        #         # Make sure not to draw label too close to top of window
        #         label_ymin = max(ymin, labelSize[1] + 10)
        #         cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (
        #             xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
        #         cv2.putText(frame, label, (xmin, label_ymin-7),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
        # if time.time() - start >= 1:
        #     print('fps:', frame_counter)
        #     frame_counter = 0
        #     start = time.time()
        
        cv2.imshow('Object detector', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

main()