import tkinter as tk
import components.face_smoother as fs
import components.image_resizer as ir
import components.file_manager as fman
import components.frame_manager as fm
import components.color_corrector as cc

COLOR_BG = "#181818"
COLOR_TEXT = "#D9D9D9"

def save_image(w_entry,h_entry,img,win):
    width = int(w_entry.get())
    height = int(h_entry.get())
    
    resized_img = ir.resize_image(img,(width,height))
    fman.save_image(resized_img)

    win.destroy()
   
def save_bulk(w_entry, h_entry, imgs, win, commands):
    width = int(w_entry.get())
    height = int(h_entry.get())
    res = []
    for img in imgs:
        img_to_add = img.copy()
        for comm in commands:            
            match comm[0]:
                case "remove blemish":
                    temp_img, face = fs.detect_face(img_to_add)
                    img_to_add = fs.apply_face_smoothing(temp_img,face)
                case "framing":
                    img_to_add = fm.overlay(fman.get_rgb_from_bgr(img_to_add),comm[1])                    
                case "color correction":
                    for corr in comm[1]:
                        if corr[0] == "Temperature":
                            print("Temp")
                        elif corr[0] == "Brightness":
                            print("bright")
                        elif corr[0] == "Saturation":
                            print("satur")

        img_to_add = ir.resize_image(fman.get_bgr_from_rgb(img_to_add),(width,height))
        res.append(img_to_add)
        
    fman.save_images(res)
    win.destroy()


def open_popup(w, h, img, commands):
    window = tk.Tk()
    window.title("Input Dimensions")
    window.configure(bg = COLOR_BG)
 


    prompt_label_1 = tk.Label(window,
                              text=f"Enter image dimensions you want to save",
                              bg = COLOR_BG,
                              fg=COLOR_TEXT)
    prompt_label_1.grid(row=0, columnspan=2, column=0, padx=10, pady=5)

    prompt_label_2 = tk.Label(window,
                              text=f"Original Dimensions: W = {w}, H = {h})",
                              bg = COLOR_BG,
                              fg=COLOR_TEXT)
    prompt_label_2.grid(row=1, columnspan=2, column=0, padx=10, pady=5)

    

    # Create labels and entry boxes for width and height
    width_label = tk.Label(window,
                           text="Width:",
                           bg = COLOR_BG,
                           fg=COLOR_TEXT)
    width_label.grid(row=2, column=0, padx=10, pady=5)
    width_entry = tk.Entry(window, bg = COLOR_BG, fg=COLOR_TEXT)
    width_entry.grid(row=2, column=1, padx=10, pady=5)


    height_label = tk.Label(window,
                            text="Height:",
                            bg = COLOR_BG,
                            fg=COLOR_TEXT)
    height_label.grid(row=3, column=0, padx=10, pady=5)
    height_entry = tk.Entry(window, bg = COLOR_BG, fg=COLOR_TEXT)
    height_entry.grid(row=3, column=1, padx=10, pady=5)

    # Create the confirm button
    confirm_button = tk.Button(window,
                               text="Confirm",
                               bg = COLOR_TEXT,
                               fg=COLOR_BG)
    confirm_button.grid(row=4, columnspan=2, padx=10, pady=10)

    if len(commands) > 0:
        confirm_button.configure(command=lambda: save_bulk(width_entry,height_entry,img,window,commands))
    else:
        confirm_button.configure(command=lambda: save_image(width_entry,height_entry,img,window))
    # Run the Tkinter event loop
    window.mainloop()    