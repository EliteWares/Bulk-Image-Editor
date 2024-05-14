import tkinter
import tkinter.filedialog
import tkinter.messagebox
import customtkinter
import os
import src.frame_manager as fm
import src.face_smoother as fs
import src.image_resizer as ir
import src.file_manager as fman
import src.color_corrector as cc
import src.save_popup as pup

from pathlib import Path
from PIL import Image, ImageTk

PREVIEW_HEIGHT = 900.0
PREVIEW_WIDTH = 300.0
APP_WIDTH = 1000
APP_HEIGHT = 600
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../imgs/res")

customtkinter.set_appearance_mode("Dark")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class BulkImageEditor(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Bulk Image Editor")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.configure(bg = "#181818")
        
        # set grid layout 1x3
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
                
       
        self.color_cor = None
        self.display_image = None
        self.file_path = ""
        self.command_list = []
        self.color_corr_commands = []
        self.image_history = []
        self.images = []
        self.orig_img_shapes = []

        
    def start(self):
        self.create_widgets()
        self.mainloop()
          
    
    def upload_folder(self):
        currdir = os.getcwd()
        
        folder_path = tkinter.filedialog.askdirectory(parent=self,
                                                   initialdir= currdir,
                                                   title="Select folder of images")
        
        if not folder_path:
            return
        
        self.images = fman.get_rgb_from_folder(folder_path)
        self.orig_img_shapes = []
        for img in self.images:
            self.orig_img_shapes.append(img.shape)
            
        self.display_image = ir.resize_to_preview(self.images[0].copy())
        self.image_history = [self.display_image.copy()]
        
        self.update_preview()
    
    def remove_blemish(self):
        self.command_list.append(["remove blemish"])
        
        image, face = fs.detect_face(self.image_history[-1].copy())
        self.display_image = fs.apply_face_smoothing(image,face)
        
        self.image_history.append(self.display_image.copy())

        self.update_preview()
    

    def confirm_color_corr(self):
        if self.corr_label.cget("text") == "Saturation" and self.slider.get() != 1:
            self.image_history.append(self.display_image.copy())
            self.color_corr_commands.append([self.corr_label.cget("text"),self.slider.get()])
        elif self.corr_label.cget("text") != "Saturation" and self.slider.get() != 0:
            self.image_history.append(self.display_image.copy())
            self.color_corr_commands.append([self.corr_label.cget("text"),self.slider.get()])

        if len(self.color_corr_commands) > 0:
            for comm in self.color_corr_commands:
                self.command_list.append(comm)
        print(f"Command List = {self.command_list}")
        
        self.hide_color_corr_panel()

    def framing(self):
        if len(self.image_history) == 0: return

        overlay_path = ""
        
        currdir = os.getcwd()
        overlay_path = tkinter.filedialog.askopenfilename(parent=self, initialdir=currdir, title='Select Frame Image',)
        
        if not overlay_path:
            return
        
        self.command_list.append(["framing",overlay_path])
        

        self.display_image = fm.overlay(self.display_image,overlay_path)
        self.image_history.append(self.display_image.copy())

        self.update_preview()
    
    
    def adjust_image(self, val):
        corr_type = self.corr_label.cget("text")

        match corr_type:
            case "Temperature":
                self.display_image = cc.adjust_temperature(val,self.image_history[-1])                
            case "Brightness":
                self.display_image = cc.adjust_brightness(val,self.image_history[-1])                
            case "Contrast":
                self.display_image = cc.adjust_contrast(val,self.image_history[-1])                
            case "Highlights":
                self.display_image = cc.adjust_highlights(val,self.image_history[-1])                
            case "Shadows":
                self.display_image = cc.adjust_shadows(val,self.image_history[-1])                
            case "Saturation":
                self.display_image = cc.adjust_saturation(val,self.image_history[-1])   

        self.update_preview()

    def change_mode(self,mode):
        if self.corr_label.cget("text") == "Saturation" and self.slider.get() != 1:
            self.image_history.append(self.display_image.copy())
            self.color_corr_commands.append([self.corr_label.cget("text"),self.slider.get()])
            self.slider.set(1)
        elif self.corr_label.cget("text") != "Saturation" and self.slider.get() != 0:
            self.image_history.append(self.display_image.copy())
            self.color_corr_commands.append([self.corr_label.cget("text"),self.slider.get()])
            self.slider.set(0)
        
        print(f"Color Correction command List = {self.color_corr_commands}")
        
        match mode:
            case "temperature":
                self.corr_label.configure(text="Temperature")
                self.slider.configure(from_=-25, to=25)
            case "brightness":
                self.corr_label.configure(text="Brightness")
                self.slider.configure(from_=-100, to=100)
            case "contrast":
                self.corr_label.configure(text="Contrast")
                self.slider.configure(from_=-100, to=100)
            case "saturation":
                self.corr_label.configure(text="Saturation")
                self.slider.configure(from_=0, to=2)
            case "highlights":
                self.corr_label.configure(text="Highlights")
                self.slider.configure(from_=-100, to=100)
            case "shadows":
                self.corr_label.configure(text="Shadows")
                self.slider.configure(from_=-100, to=100)
        

                
    def undo(self):
        if self.corr_label._text == "Saturation":
            if self.slider.get() != 1:
                self.slider.set(1)
        else:
            if self.slider.get() != 0:
                self.slider.set(0)
        
        self.adjust_image(self.slider.get())
           
        if len(self.color_corr_commands) > 0:
            self.color_corr_commands.pop()
            self.image_history.pop()
            return

        if len(self.image_history) > 1:
            self.image_history.pop()
            self.display_image = self.image_history[-1].copy()
        
            if len(self.command_list) > 0: self.command_list.pop()
    
        self.update_preview()

    def save(self):
       '''pup.open_popup(self.orig_img_shapes[0][1],
                      self.orig_img_shapes[0][0],
                      self.images,
                      self.command_list)'''
       save_popup = pup.SavePopUp(self.images,self.orig_img_shapes,self.command_list)
       save_popup.mainloop()
        

    def update_preview(self):
        h,w,_ = self.display_image.shape
        ctk_img = customtkinter.CTkImage(Image.fromarray(self.display_image),size=(w,h))
        self.image_label.configure(image=ctk_img, text= "")
    
    def show_color_corr_panel(self):
        self.color_cor_frame.grid(row=0, column=3, sticky="nse")
        self.color_cor_btn.configure(command=self.hide_color_corr_panel)

        self.display_image = self.image_history[-1].copy()
        self.image_history.append(self.display_image.copy())
        self.color_corr_commands = []
    
    def hide_color_corr_panel(self):
        self.color_cor_frame.grid_forget()
        self.color_cor_btn.configure(command=self.show_color_corr_panel)

        

    def create_widgets(self):
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame.grid(row=0, column=0, sticky="nsw")

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Bulk Image Editor",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
    
        # Create Navigation Buttons
        self.blemish_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Remove Blemishes",
                                                   fg_color="transparent", text_color=("red", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=self.remove_blemish)
        self.blemish_btn.grid(row=1, column=0, sticky="ew")

        self.color_cor_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Color Correction",
                                                   fg_color="transparent", text_color=("red", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=self.show_color_corr_panel)
        self.color_cor_btn.grid(row=2, column=0, sticky="ew")

        self.frame_mngr_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame Manager",
                                                   fg_color="transparent", text_color=("red", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=self.framing)
        self.frame_mngr_btn.grid(row=3, column=0, sticky="ew")

        self.undo_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Undo",
                                                   fg_color="transparent", text_color=("red", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=self.undo)
        self.undo_btn.grid(row=4, column=0, sticky="ew")

        self.save_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Save",
                                                   fg_color="transparent", text_color=("red", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=self.save)
        self.save_btn.grid(row=5, column=0, sticky="ew")

        self.upload_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=5, height=40, border_spacing=10, text="Upload Folder",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#766BED"),
                                                   command=self.upload_folder)
        self.upload_btn.grid(row=6, column=0, sticky="s")
        self.upload_btn.grid_configure(pady=(0,50))

        # create Image frame
        self.img_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.img_frame.grid_rowconfigure(0, weight=1)
        self.img_frame.grid(row=0, column=2)
        
        
        # Add Preview image to image frame
        
        #ctk_img = customtkinter.CTkImage(Image.fromarray(self.image_history[-1]),size=(self.w,self.h))

        self.image_label = customtkinter.CTkLabel(self.img_frame,text="Upload a folder to show preview")
        self.image_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # Add color correction frame
        self.color_cor_frame = customtkinter.CTkFrame(self, corner_radius=0)
        
        self.color_cor_frame.grid_rowconfigure(8, weight=1)
        

        self.corr_label = customtkinter.CTkLabel(self.color_cor_frame,text="Temperature",font=("Times New Roman",20,"bold"))
        self.corr_label.grid(row=0, column=0, padx=20, pady=20)

        # Add slider to color corr frame
        self.slider = customtkinter.CTkSlider(self.color_cor_frame,
                                             from_=-25,
                                             to=25,
                                             progress_color="#766BED",
                                             fg_color="#766BED",
                                             button_color="#A364FF",
                                             command=self.adjust_image)
        self.slider.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider.grid_configure(pady=50)
        self.slider.set(0)
        # Add buttons for color correction to frame
        
        self.temp_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=0, height=40, border_spacing=10, text="Temperature",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=lambda: self.change_mode("temperature"))
        self.temp_btn.grid(row=2, column=0, sticky="ew")

        self.bright_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=0, height=40, border_spacing=10, text="Brightness",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=lambda: self.change_mode("brightness"))
        self.bright_btn.grid(row=3, column=0, sticky="ew")
        
        self.contr_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=0, height=40, border_spacing=10, text="Contrast",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=lambda: self.change_mode("contrast"))
        self.contr_btn.grid(row=4, column=0, sticky="ew")

        self.high_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=0, height=40, border_spacing=10, text="Highlights",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=lambda: self.change_mode("highlights"))
        self.high_btn.grid(row=5, column=0, sticky="ew")
        
        self.shad_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=0, height=40, border_spacing=10, text="Shadows",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=lambda: self.change_mode("shadows"))
        self.shad_btn.grid(row=6, column=0, sticky="ew")
        
        self.satur_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=0, height=40, border_spacing=10, text="Saturation",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#A364FF"),
                                                   command=lambda: self.change_mode("saturation"))
        self.satur_btn.grid(row=7, column=0, sticky="ew")

        self.confirm_btn = customtkinter.CTkButton(self.color_cor_frame, corner_radius=5, height=40, border_spacing=10, text="Confirm",
                                                   fg_color="transparent", text_color=("gray70", "gray90"), hover_color=("gray70", "#766BED"),
                                                   command=self.confirm_color_corr)
        self.confirm_btn.grid(row=8, column=0, sticky="s")
        self.confirm_btn.grid_configure(pady=20)
        
   
