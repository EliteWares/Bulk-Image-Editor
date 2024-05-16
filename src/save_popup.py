import tkinter
import tkinter.messagebox
import customtkinter
import cv2 as cv


import src.face_smoother as fs
import src.image_resizer as ir
import src.file_manager as fman
import src.frame_manager as fm
import src.color_corrector as cc
#import face_smoother as fs
#import image_resizer as ir
#import file_manager as fman
#import frame_manager as fm
#import color_corrector as cc

      

class SavePopUp(customtkinter.CTk):
    def __init__(self,images,original_shapes,commands):
        super().__init__()
        # configure window
        self.title("Save Dimensions")
        self.geometry(f"{525}x{400}")
        self.progress = 0
        self.progress_incr = 0

        self.images = images
        self.orig_shapes = original_shapes
        self.commands = commands

        

        self.top_frame = customtkinter.CTkFrame(self, fg_color="transparent")

        self.label = customtkinter.CTkLabel(self.top_frame,
                                            text="Enter dimensions you wish to save images as or use original dimensions. (in pixels)")

        self.w_entry = customtkinter.CTkEntry(self.top_frame,placeholder_text="Width")
        self.h_entry = customtkinter.CTkEntry(self.top_frame,placeholder_text="Height")
               

        self.bot_frame = customtkinter.CTkFrame(self,fg_color="transparent")

        self.custom_save_btn = customtkinter.CTkButton(self.bot_frame,text="Save custom dimensions",
                                                       fg_color="transparent", text_color=("red", "gray90"),
                                                       hover_color=("gray70", "#A364FF"), corner_radius=0,
                                                       height=40, border_spacing=10,command=lambda:self.save("custom"))
        self.origin_save_btn = customtkinter.CTkButton(self.bot_frame,text="Save original dimensions",
                                                       fg_color="transparent", text_color=("red", "gray90"),
                                                       hover_color=("gray70", "#A364FF"), corner_radius=0,
                                                       height=40, border_spacing=10,command=lambda:self.save("original"))

        self.progressbar = customtkinter.CTkProgressBar(self.bot_frame,width=200,height=20,progress_color="#A364FF")
        
        self.grid_rowconfigure(2, weight=0,pad=30)
        self.top_frame.grid_rowconfigure(0)
        self.bot_frame.grid_rowconfigure(1)

        self.top_frame.grid(row=0,pady=25)
        self.bot_frame.grid(row=1,sticky="s")
        self.label.grid(row=0,padx=25,pady=15)
        self.w_entry.grid(row=1,pady=(0,10))
        self.h_entry.grid(row=2,pady=(10,0))
        self.custom_save_btn.grid(row=0)
        self.origin_save_btn.grid(row=1)
        
    
    def save(self, type):
        if type == "custom":
            width = int(self.w_entry.get())
            height = int(self.h_entry.get())
            if not width or not height:
                return
            
        save_path = tkinter.filedialog.askdirectory(title="Choose export folder")
        if not save_path:
            return
        

        self.progressbar.grid(row=2, pady=20, sticky="ew")
        self.progressbar.set(0)
        
        save_label = customtkinter.CTkLabel(self.bot_frame,text="Saving ...")
        save_label.grid(row=3)
        self.progress_incr = 1 / len(self.images)
        

        for i in range(len(self.images)):
            self.show_progress()

            edited_img = self.images[i].copy()
            for comm in self.commands:            
                match comm[0]:
                    case "remove blemish":
                        temp_img, face = fs.detect_face(edited_img)
                        edited_img = fs.apply_face_smoothing(temp_img,face)
                    case "framing":
                        edited_img = fm.overlay(edited_img,comm[1])
                    case "Temperature":
                        edited_img = cc.adjust_temperature(comm[1],edited_img)
                    case "Brightness":
                        edited_img = cc.adjust_brightness(comm[1],edited_img)
                    case "Contrast":
                        edited_img - cc.adjust_contrast(comm[1],edited_img)
                    case "Highlights":
                        edited_img - cc.adjust_highlights(comm[1],edited_img)
                    case "Shadows":
                        edited_img - cc.adjust_shadows(comm[1],edited_img)
                    case "Saturation":
                        edited_img = cc.adjust_saturation(comm[1],edited_img)

            if type == "original":
                height,width,_ = self.orig_shapes[i]
                
            edited_img = ir.resize_image(edited_img,(width,height))

            path = save_path + f"/export-{i}.png"
            cv.imwrite(filename=path,img=fman.get_bgr_from_rgb(edited_img))
        
        self.destroy()
 
    def show_progress(self):
        print("update")
        self.progress += self.progress_incr
        self.progressbar.set(self.progress)
