from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
import subprocess
import os
import components.frame_manager as fm
import components.face_smoother as fs
import components.image_resizer as ir
import components.color_corrector as cc
import components.exposure as exp
import components.popup as pup
import components.test as test

PREVIEW_HEIGHT = 900.0
PREVIEW_WIDTH = 300.0
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../imgs/res")

class BatchImageEditor:
    def __init__(self, root:Tk):
        self.window = root
        self.window.title("Image Adjustment")
        self.window.geometry("1280x720")
        self.window.configure(bg = "#181818")
        self.window.resizable(False, False)
        self.color_cor = None
        self.input_path = ""
        self.image_history = []
        self.orig_img_height = 0.0
        self.orig_img_width = 0.0

    def start(self):
        self.create_widgets()
        self.window.mainloop()
    
    def relative_to_assets(self,path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def update_preview(self):
        imgtk = ImageTk.PhotoImage(image = Image.fromarray(self.image_history[-1]))
        self.canvas.create_image(
            933.0,
            390.0,
            image=imgtk
        )
        self.window.mainloop()
    
    def upload_image(self):
        currdir = os.getcwd()
        
        self.input_path = filedialog.askopenfilename(parent=self.window,
                                                     initialdir=currdir,
                                                     title='Please select a directory',
                                                     filetypes=[('image files',('.png','.jpeg','.jpg'))]
                                                     )
        image = ir.get_rgb_from_path(self.input_path)
        self.orig_img_height, self.orig_img_width, _ = image.shape
        img_copy = image.copy()
        self.image_history = [ir.resize_to_preview(img_copy)]

        self.update_preview()
    
    def remove_blemish(self):
        image, face = fs.detect_face(self.image_history[-1].copy())
        current_img = fs.apply_face_smoothing(image,face)
        self.image_history.append(current_img)

        #subprocess.run(['python', 'components/blemish_remover.py', input_path])

        self.update_preview()
    
    def get_corrected_img(self):
        self.image_history.append(self.color_cor.image)
        self.color_cor.master.destroy()
        self.update_preview()
        

    def color_correction(self):
        self.color_cor = cc.open_popup(self.image_history[-1])
        self.btn = self.color_cor.get_btn()
        self.btn.configure(command=self.get_corrected_img)
        
    
    def framing(self):
        currdir = os.getcwd()
        overlay_path = filedialog.askopenfilename(parent=self.window, initialdir=currdir, title='Select Frame Image',)
        
        current_img = fm.overlay(self.image_history[-1],overlay_path)
        self.image_history.append(current_img)

        self.update_preview()
    
    def undo(self):
        if len(self.image_history) > 1:
            self.image_history.pop()
    
        self.update_preview()
    
    def save(self):
        pup.dimensions_popup(self.orig_img_width,self.orig_img_height,self.image_history[-1])


    def configure_button(self,button, reg_btn, hov_btn, dim, pos):
        img_hov = PhotoImage(file=self.relative_to_assets(hov_btn))
        img_reg = PhotoImage(file=self.relative_to_assets(reg_btn))
            
        button.bind("<Enter>", func=lambda e: button.config(image=img_hov))
        button.bind("<Leave>", func=lambda e: button.config(image=img_reg))

        button.place(
            x=pos[0],
            y=pos[1],
            width=dim[0],
            height=dim[1]
        )    

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg = "#181818",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.create_text(
            443.0,
            32.0,
            anchor="nw",
            text="Bulk Image Editor",
            fill="#A364FF",
            font=("Inter", 36 * -1)
        )
        self.canvas.place(x = 0, y = 0)
        self.canvas.pack()

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.undo,
            relief="flat",
            name="undo"
        )
        self.configure_button(button = button_1,
                        reg_btn = "button_1.png",
                        hov_btn = "button_1_hover.png",
                        dim = (81.0,81.0),
                        pos = (555.0,351.0))


        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.save,
            relief="flat",
            background="#181818",
            name="save"
        )
        self.configure_button(button = button_2,
                        reg_btn = "button_2.png",
                        hov_btn = "button_2_hover.png",
                        dim = (201.0,69.0),
                        pos = (238.0,613.0))

        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.framing,
            relief="flat",
            background="#181818",
            name="framing"
        )
        self.configure_button(button = button_3,
                        reg_btn = "button_3.png",
                        hov_btn = "button_3_hover.png",
                        dim = (268.0,78.0),
                        pos = (207.0,460.0))

        self.button_image_4 = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command= self.color_correction,
            relief="flat",
            background="#181818",
            name="color_corr"
        )
        self.configure_button(button = button_4,
                        reg_btn = "button_4.png",
                        hov_btn = "button_4_hover.png",
                        dim = (268.0,78.0),
                        pos = (207.0,351.0))

        self.button_image_5 = PhotoImage(
            file=self.relative_to_assets("button_5.png"))
        button_5 = Button(
            image=self.button_image_5,
            borderwidth= 0,
            highlightthickness= 0,
            command= self.remove_blemish,
            relief= "flat",
            background= "#181818",
            name= "blemish"
        )
        self.configure_button(button = button_5,
                        reg_btn = "button_5.png",
                        hov_btn = "button_5_hover.png",
                        dim = (268.0,82.0),
                        pos = (207.0,242.0))

        self.button_image_6 = PhotoImage(
            file=self.relative_to_assets("button_6.png"))
        button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Upload folder"),
            relief="flat",
            background="#181818",
            name="upload_folder",
            
        )
        self.configure_button(button = button_6,
                        reg_btn = "button_6.png",
                        hov_btn = "button_6_hover.png",
                        dim = (189.0,78.0),
                        pos = (352.0,137.0))

        self.button_image_7 = PhotoImage(
            file=self.relative_to_assets("button_7.png"))
        button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.upload_image,
            relief="flat",
            background="#181818",
            name="upload_image"
        )
        self.configure_button(button = button_7,
                        reg_btn = "button_7.png",
                        hov_btn = "button_7_hover.png",
                        dim = (189.0,78.0),
                        pos = (135.0,137.0))