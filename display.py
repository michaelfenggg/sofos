import tkinter as tk
from PIL import Image, ImageTk
import time

# Create the main window
root = tk.Tk()
root.geometry("800x480")

# Create the logo
image = Image.open("sofos.png")
photo_image = ImageTk.PhotoImage(image)
sofos = tk.Label(root, image = photo_image)
sofos.place(x=0,y=0)

root.mainloop()
