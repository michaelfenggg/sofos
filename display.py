import tkinter as tk
from PIL import Image, ImageTk
import tk_tools
import time
import matplotlib

# Create the main window
root = tk.Tk()
root.geometry("800x480")
root.configure(bg = "white")

# Create the logo
image = Image.open("sofos.png")
photo_image = ImageTk.PhotoImage(image)
sofos = tk.Label(root, image = photo_image)
sofos.place(relx = 0, rely = 1, anchor = "sw")

greeting = tk.Label(root, text = "Good afternoon Thea!", font = ("Inter", 35), padx = 10, wraplength = 300, justify = 'left')
greeting.configure(bg = "white")
greeting.place(relx = 0, rely = 0.5, anchor = "w")

def countdown():
    global timer
    if timer <= 20:
        label.config(text=f"{timer:02} sec", font = ("Inter", 35))
        timer += 1
        progress.set_value(timer / 20)
        root.after(1000, countdown)

timer = 0
label = tk.Label(root, text = f"{timer:02}")
label.configure(bg = "white")
label.place(relx = 1, rely = 1, anchor = "se")

progress = tk_tools.RotaryScale(root, max_value = 7, size = 100, unit = "progress")
progress.place(relx = 1, rely = 0.5, anchor = "w")
progress.set_value(0)

countdown()
print("Matplotlib Version : {}".format(matplotlib.__version__))
root.mainloop()
