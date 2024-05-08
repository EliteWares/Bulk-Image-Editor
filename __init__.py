from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
import subprocess
import os
import components.frame_manager as fm
import components.face_smoother as fs
import components.image_resizer as ir

# Figma Token = figd_PO7Yp3W-flDKHxANy3QQGEW0gwi_g2VYd_CNM7mW

input_path = ""
image_history = []

PREVIEW_HEIGHT = 900.0
PREVIEW_WIDTH = 300.0
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"imgs/res")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

  
def upload_image():
    global input_path, canvas, window, image_history

    currdir = os.getcwd()
    input_path = filedialog.askopenfilename(parent=window, initialdir=currdir, title='Please select a directory',filetypes=[('image files',('.png','.jpeg','.jpg'))])
    current_img = ir.get_rgb_from_path(input_path)
    img_copy = current_img.copy()
    image_history = [ir.resize_to_preview(img_copy)]

    imgtk = ImageTk.PhotoImage(image = Image.fromarray(image_history[-1]))
    canvas.create_image(
        933.0,
        390.0,
        image=imgtk
    )
    window.mainloop()

def remove_blemish(canvas,window):
    global image_history
    image, face = fs.detect_face(image_history[-1].copy())
    current_img = fs.apply_face_smoothing(image,face)
    image_history.append(current_img)
    #subprocess.run(['python', 'components/blemish_remover.py', input_path])
    
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(image_history[-1]))
    canvas.create_image(
        933.0,
        390.0,
        image=imgtk
    )
    window.mainloop()

def color_correction():
    pass

def framing(canvas,window):
    global image_history
    currdir = os.getcwd()
    overlay_path = filedialog.askopenfilename(parent=window, initialdir=currdir, title='Select Frame Image',)
    
    current_img = fm.overlay(image_history[-1],overlay_path)
    image_history.append(current_img)

    imgtk = ImageTk.PhotoImage(image = Image.fromarray(image_history[-1]))
    canvas.create_image(
        933.0,
        390.0,
        image=imgtk
    )
    window.mainloop()

def sizing():
    pass

def undo():
    global image_history
    if len(image_history) > 1:
        image_history.pop()
  
    imgtk = ImageTk.PhotoImage(image = Image.fromarray(image_history[-1]))
    canvas.create_image(
        933.0,
        390.0,
        image=imgtk)
    window.mainloop()

def save():
    ir.save(image_history[-1])

def changeOnHover(button, reg_btn, hov_btn):
    

    img_hov = PhotoImage(file=relative_to_assets(hov_btn))
    img_reg = PhotoImage(file=relative_to_assets(reg_btn))
    
    #hov_shape = ir.get_rgb_from_path(f"imgs/res/{hov_btn}").shape
    #reg_shape = ir.get_rgb_from_path(f"imgs/res/{reg_btn}").shape
    
    #print(f"Hover shape: {hov_shape}, Regular shape: {reg_shape}")
    
    button.bind("<Enter>", func=lambda e: button.config(image=img_hov))
    button.bind("<Leave>", func=lambda e: button.config(image=img_reg))
    

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
    command=undo,
    relief="flat",
    name="undo"
)
button_1.place(
    x=555.0,
    y=351.0,
    width=81.0,
    height=81.0
)
changeOnHover(button_1,"button_1.png","button_1_hover.png")


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=save,
    relief="flat",
    background="#181818",
    name="save"
)
button_2.place(
    x=238.0,
    y=613.0,
    width=201,
    height=69.0
)
changeOnHover(button_2,"button_2.png","button_2_hover.png")

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: framing(canvas, window),
    relief="flat",
    background="#181818",
    name="framing"
)
button_3.place(
    x=207.0,
    y=460.0,
    width=268.0,
    height=78.0
)
changeOnHover(button_3,"button_3.png","button_3_hover.png")

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command= color_correction,
    relief="flat",
    background="#181818",
    name="color_corr"
)
button_4.place(
    x=207.0,
    y=351.0,
    width=268.0,
    height=78.0
)
changeOnHover(button_4,"button_4.png","button_4_hover.png")

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: remove_blemish(canvas,window),
    relief="flat",
    background="#181818",
    name="blemish"
)
button_5.place(
    x=207.0,
    y=242.0,
    width=268.0,
    height=82.0
)
changeOnHover(button_5,"button_5.png","button_5_hover.png")

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Upload folder"),
    relief="flat",
    background="#181818",
    name="upload_folder",
    
)
button_6.place(
    x=352.0,
    y=137.0,
    width=189.0,
    height=78.0
)
changeOnHover(button_6,"button_6.png","button_6_hover.png")

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=upload_image,
    relief="flat",
    background="#181818",
    name="upload_image"
)
button_7.place(
    x=135.0,
    y=137.0,
    width=189.0,
    height=78.0
)
changeOnHover(button_7,"button_7.png","button_7_hover.png")


'''image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    933.0,
    390.0,
    image=image_image_1
)'''

if __name__ == "__main__":
    
    canvas.place(x = 0, y = 0)
    canvas.create_text(
        443.0,
        32.0,
        anchor="nw",
        text="Bulk Image Editor",
        fill="#A364FF",
        font=("Inter", 36 * -1)
    )
    canvas.pack()
    window.resizable(False, False)
    window.mainloop()
