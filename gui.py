
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
import subprocess
import os
import components.frame_manager as fm
import components.face_smoother as fs
input_path = ""

PREV_HEIGHT = 900.0
PREV_WIDTH = 300.0
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\chukw\Documents\UWI Courses\COMP3901 - Capstone Project\figma-design\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def select_upload_folder():
    global input_path,window,canvas
    currdir = os.getcwd()
    input_path = filedialog.askopenfilename(parent=window, initialdir=currdir, title='Please select a directory',)

    input_img = PhotoImage(file=relative_to_assets(input_path))

    canvas.create_image(
        944.0,
        398.0,
        image=input_img
    )
    window.mainloop()

def remove_blemish():
    image, face = fs.detect_face(input_path)
    smooth_img = fs.apply_face_smoothing(image,face)
    #fs.draw_squares(smooth_img,face)
    #subprocess.run(['python', 'components/blemish_remover.py', input_path])
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(smooth_img))
    canvas.create_image(
        944.0,
        398.0,
        image=imgtk
    )
    window.mainloop()

def color_correction():
    pass

def framing(canvas,window):
    currdir = os.getcwd()
    overlay = filedialog.askopenfilename(parent=window, initialdir=currdir, title='Select Frame Image',)

    img = fm.overlay(input_path,overlay)
    
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(img))
    canvas.create_image(
        944.0,
        398.0,
        image=imgtk
    )
    window.mainloop()

def sizing():
    pass

window = Tk()
window.geometry("1280x720")
window.configure(bg = "#181818")

canvas = Canvas(
    window,
    bg = "#181818",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    443.0,
    32.0,
    anchor="nw",
    text="Bulk Image Editor",
    fill="#A364FF",
    font=("Inter", 36 * -1)
)
'''
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    944.0,
    398.0,
    image=image_image_1
)
'''

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=sizing,
    relief="flat"
)
button_1.place(
    x=207.0,
    y=569.0,
    width=236.0,
    height=61.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: framing(canvas, window),
    relief="flat"
)
button_2.place(
    x=207.0,
    y=460.0,
    width=236.0,
    height=61.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=color_correction,
    relief="flat"
)
button_3.place(
    x=207.0,
    y=351.0,
    width=236.0,
    height=61.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command= remove_blemish,
    relief="flat"
)
button_4.place(
    x=207.0,
    y=242.0,
    width=236.0,
    height=61.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=select_upload_folder,
    relief="flat"
)
button_5.place(
    x=207.0,
    y=133.0,
    width=236.0,
    height=61.0
)

window.resizable(False, False)
window.mainloop()