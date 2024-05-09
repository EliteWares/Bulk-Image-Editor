import tkinter as tk
import components.image_resizer as ir

    

def confirm_dimensions(w_entry,h_entry,img,win):
    width = int(w_entry.get())
    height = int(h_entry.get())
    
    resized_img = ir.resize_image(img,(width,height))
    ir.save(resized_img)

    win.destroy()
    

# Create the main window
def dimensions_popup(w, h, img):
    window = tk.Tk()
    window.title("Input Dimensions")
    window.configure(bg = "#181818")
 


    prompt_label_1 = tk.Label(window,
                              text=f"Enter image dimensions you want to save",
                              bg = "#181818",
                              fg="#A364FF")
    prompt_label_1.grid(row=0, columnspan=2, column=0, padx=10, pady=5)

    prompt_label_2 = tk.Label(window,
                              text=f"Original Dimensions: W = {w}, H = {h})",
                              bg = "#181818",
                              fg="#A364FF")
    prompt_label_2.grid(row=1, columnspan=2, column=0, padx=10, pady=5)

    

    # Create labels and entry boxes for width and height
    width_label = tk.Label(window,
                           text="Width:",
                           bg = "#181818",
                           fg="#A364FF")
    width_label.grid(row=2, column=0, padx=10, pady=5)
    width_entry = tk.Entry(window, bg = "#181818", fg="white")
    width_entry.grid(row=2, column=1, padx=10, pady=5)


    height_label = tk.Label(window,
                            text="Height:",
                            bg = "#181818",
                            fg="#A364FF")
    height_label.grid(row=3, column=0, padx=10, pady=5)
    height_entry = tk.Entry(window, bg = "#181818", fg="white")
    height_entry.grid(row=3, column=1, padx=10, pady=5)

    # Create the confirm button
    confirm_button = tk.Button(window,
                               text="Confirm",
                               command=lambda: confirm_dimensions(width_entry,height_entry,img,window),
                               bg = "#181818",
                               fg="#A364FF")
    confirm_button.grid(row=4, columnspan=2, padx=10, pady=10)

    # Run the Tkinter event loop
    window.mainloop()    