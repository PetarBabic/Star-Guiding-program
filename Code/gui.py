from tkinter import * 
import tkinter as tk
from PIL import Image, ImageTk
import test
from os import execl
from sys import executable, argv
import time
import camera

starSelectBool = False
downsample = 1

def ConsoleInput(txt, fontColor):
    global text
    
    text.config(state=NORMAL, fg=fontColor)
    text.delete('1.0', END)
    text.insert(INSERT, txt)
    text.config(state=DISABLED)

def SelectStar():
    global label, starSelectBool
    ConsoleInput("Status: Selecting a star", "white")
    
    if(not starSelectBool):
        label.bind("<Button-1>", ClickEvent)
        label.configure(cursor="icon")
    else:
        label.unbind("<Button-1>")
        label.configure(cursor="arrow")
        
    starSelectBool = not starSelectBool

def StartGuiding():
    global image
    ConsoleInput("Status: Calibrating", "#34D321")
    test.Calibrate(image)
    ConsoleInput("Status: Guiding", "#34D321")
    test.Guide()

def StopGuiding():
    ConsoleInput("Status: Guiding stopped", "red")

def ClickEvent(event):
    global downsample, text, starSelectBool
    
    # Check if a star has been found in the selected roi
    if(test.StarSelect(event.x * downsample, event.y * downsample)):
        ConsoleInput("Status: Found a star", "#34D321")
        
        # Disable clickable label
        label.unbind("<Button-1>")
        # Change back to og mouse cursor
        label.configure(cursor="arrow")
        
        starSelectBool = not starSelectBool
        
    else:
        ConsoleInput("Status: No stars found", "red")

def Restart():
    python = executable
    execl(python, python, * argv)

def test2():
    test.angle = 135

    test.pulseStrenghtDir[0] = 0.788
    test.pulseStrenghtDir[1] = 0.788
    test.pulseStrenghtDir[2] = 0.788
    test.pulseStrenghtDir[3] = 0.788

    test.Guide()


image = camera.capture(1, 75)

root = tk.Tk()
# Windows size when app is opened
root.geometry('500x500')
# Window name
root.title('Guider')

# Canvas size, increase if image isn't displayed properly
canvas = tk.Canvas(root, height=1500, width=1500)
canvas.pack()

# Black rectangle at bootom of frame
frame = tk.Frame(root, bg="black")
frame.place(rely = 0.8, relwidth = 1, relheight=1)

# Buttons to:
#   to select a star
selectStarButton = tk.Button(root, text="Select a Star", highlightbackground = "blue", highlightcolor= "black", command=SelectStar)
selectStarButton.place(relx=0, rely=0.8, width=150)
#   start guiding
startGuidingButton = tk.Button(root, text="Start Guiding", highlightbackground = "green", highlightcolor= "green", command=StartGuiding)
startGuidingButton.place(relx=0, rely=0.85, width=150)
#   stop guiding
stopGuidingButton = tk.Button(root, text="Stop Guiding", highlightbackground = "red", highlightcolor= "black", command=StopGuiding)
stopGuidingButton.place(relx=0, rely=0.9, width=150)
#   to restart the app
restartButton = tk.Button(root, text="R", highlightbackground = "black", highlightcolor= "black", command=Restart)
restartButton.place(relx=0.95, rely=0.95)

# Start test guide
testGuide = tk.Button(root, text="S", highlightbackground = "black", highlightcolor= "black", command=test2)
testGuide.place(relx=0.95, rely=0.85)

# Text that displays the status
text = Text(root, bg="black", highlightbackground = "black", highlightcolor= "black")
text.insert(INSERT, "Status: calibrating")
text.config(state=DISABLED)
text.place(relx=0, rely=0.95, width=250)

# Open the image file
image = Image.open('./image_mono.tif')
test.image = image
# If image is larger than 1000 pixels downsample it by a factor of 2
if(image.height >= 1000 or image.width >= 1000):
    image = image.resize((int(image.width / 2), int(image.height / 2)),  Image.NEAREST)
    downsample = 2

# Make it readable by tkinter
img = ImageTk.PhotoImage(image)

# Place the image using label widget
label = Label(canvas, image = img)
label.pack()

# Min window size
root.wm_minsize(image.width + 2, image.height + 120)

root.mainloop()
