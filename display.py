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
        root.after(1000, countdown)

timer = 0
label = tk.Label(root, text = f"{timer:02}")
label.configure(bg = "white")
label.place(relx = 1, rely = 1, anchor = "se")

procedures = ["Palm to palm", "Palm over dorsum, fingers interlaced", "Palm to palm, fingers interlaced",
 "Backs of fingers to opposing palm, fingers interlocked", "Rotational rubbing of the thumb", "Fingertips to palm",
 "Turning off the faucet with a paper towel"]

listbox = Listbox(root, height = 7, width = 30, bg = "white", font = ("Inter", 15), fg = "black")
listbox.insert(1, "Palm to palm")
listbox.insert(2, "Palm over dorsum, fingers interlaced")
listbox.insert(3, "Palm to palm, fingers interlaced")
listbox.insert(4, "Backs of fingers to opposing palm, fingers interlocked")
listbox.insert(5, "Rotational rubbing of the thumb")
listbox.insert(6, "Fingertips to palm")
listbox.insert(7, "Turning off the faucet with a paper towel")

def update(ind):
    listbox.delete(ind)
    listbox.insert(ind + 1, procedures[ind] + " —— DONE")

countdown()
print("Matplotlib Version : {}".format(matplotlib.__version__))
root.mainloop()
