import tkinter as tk
from PIL import Image, ImageTk
import tk_tools
import time
import matplotlib
import tkinter.font as TkFont

# Create the main window
root = tk.Tk()
root.geometry("800x480")
image1 = Image.open("bg.jpg")
image1 = ImageTk.PhotoImage(image1)
label1 = tk.Label(root, image = image1)
label1.place(x = 0,y = 0)

def countdown():
    global timer
    if timer <= 20:
        label.config(text=f"00:{timer:02} sec", font = ("Inter", 35), padx = 10, pady = 10)
        timer += 1
        root.after(1000, countdown)

def cont():
    # Create the logo
    '''
    image = Image.open("sofos.png")
    photo_image = ImageTk.PhotoImage(image)
    sofos = tk.Label(root, image = photo_image)
    sofos.place(relx = 0, rely = 1, anchor = "sw")'''
    
    font1 = TkFont.Font(family = "Inter", weight = "bold", size = 55)
    greeting = tk.Label(root, text = "Hi,\nThea!", font = font1, padx = 35, wraplength = 300, justify = 'left')
    greeting.configure(bg = "white")
    greeting.place(relx = 0, rely = 0.5, anchor = "w")
    
    timer = 0
    label = tk.Label(root, text = f"00:{timer:02}")
    label.configure(bg = "white")
    label.place(relx = 1, rely = 1, anchor = "se")
    
    procedures = ["Palm to palm", "Palm over dorsum, fingers interlaced", "Palm to palm, fingers interlaced",
     "Backs of fingers to opposing palm, fingers interlocked", "Rotational rubbing of the thumb", "Fingertips to palm",
     "Turning off the faucet with a paper towel"]
    
    todo = tk.Label(root, text = "Actions ToDo")
    font2 = TkFont.Font(family = "Inter", weight = "bold", size = 35)
    todo.config(font = font2, bg = "white", fg = "red")
    todo.place(relx = .45, rely = 0.25)
    
    listbox = tk.Listbox(root, height = 7, width = 45, bg = "white", font = ("Inter", 10), fg = "black", bd = 0)
    listbox.insert(1, "Palm to palm")
    listbox.insert(2, "Palm over dorsum, fingers interlaced")
    listbox.insert(3, "Palm to palm, fingers interlaced")
    listbox.insert(4, "Backs of fingers to opposing palm, fingers interlocked")
    listbox.insert(5, "Rotational rubbing of the thumb")
    listbox.insert(6, "Fingertips to palm")
    listbox.insert(7, "Turning off the faucet with a paper towel")
    listbox.place(relx = 0.9, rely = 0.522, anchor = 'e')
    
    countdown()

root.mainloop()
