from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
import subprocess
import os
import components.frame_manager as fm
import components.face_smoother as fs
import components.image_resizer as ir


input_path = ""
current_img = None

PREVIEW_HEIGHT = 900.0
PREVIEW_WIDTH = 300.0
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"imgs/res")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

  
def select_image():
    global input_path, current_img, canvas, window

    currdir = os.getcwd()
    input_path = filedialog.askopenfilename(parent=window, initialdir=currdir, title='Please select a directory',filetypes=[('image files',('.png','.jpeg','.jpg'))])
    current_img = ir.get_rgb_from_path(input_path)
    
    #update_preview(current_img)
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(current_img))
    canvas.create_image(
        944.0,
        398.0,
        image=imgtk
    )
    window.mainloop()

def remove_blemish(canvas,window):
    global current_img
    image, face = fs.detect_face(current_img)
    current_img = fs.apply_face_smoothing(image,face)
    #subprocess.run(['python', 'components/blemish_remover.py', input_path])
    
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(current_img))
    canvas.create_image(
        944.0,
        398.0,
        image=imgtk
    )
    window.mainloop()

def color_correction():
    pass

def framing(canvas,window):
    global current_img
    currdir = os.getcwd()
    overlay_path = filedialog.askopenfilename(parent=window, initialdir=currdir, title='Select Frame Image',)

    current_img = fm.overlay(current_img,overlay_path)
    
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(current_img))
    canvas.create_image(
        944.0,
        398.0,
        image=imgtk
    )
    window.mainloop()

def sizing():
    pass

def save():
    ir.save(current_img)



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
    command=save,
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
    command= lambda: remove_blemish(canvas,window),
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
    command=select_image,
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