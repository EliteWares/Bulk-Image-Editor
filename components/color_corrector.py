import tkinter as tk
import numpy as np
from tkinter import ttk, Label, Button
import cv2
from PIL import Image, ImageTk

class ImageAdjustmentPopup:
    def __init__(self, master, image):
        self.master = master
        self.master.title("Image Adjustment")
        
        self.image = image
        self.image_copy = self.image.copy()
        self.original_image = self.image.copy()
        self.display_image = self.image
        
        self.width, self.height, _ = self.image.shape
        
        self.brightness_value = 0
        self.saturation_value = 1.0

        self.confirm_btn = Button(self.master,text="Confirm",command=lambda: print("Confirm"))
        
        self.create_widgets()
        self.update_image()
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        
        self.image_tk = ImageTk.PhotoImage(Image.fromarray(self.display_image))
        self.canvas.create_image(0, 10, anchor=tk.NW, image=self.image_tk)
        
        self.label = Label(self.master,text="Temperature")
        self.label.pack()

        self.slider = ttk.Scale(self.master, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.adjust_temperature)
        self.slider.pack(fill=tk.X)
        self.slider
        self.slider.set(0)

        self.temp_btn = Button(self.master,text="Temperature",command=lambda: self.change_mode("temperature"))
        self.temp_btn.pack()
        self.bright_btn = Button(self.master,text="Brightness",command=lambda: self.change_mode("brightness"))
        self.bright_btn.pack()
        self.sat_btn = Button(self.master,text="Saturation",command=lambda: self.change_mode("saturation"))
        self.sat_btn.pack()
        self.confirm_btn = Button(self.master,text="Confirm",command=lambda: print("Confirm"))
        self.confirm_btn.pack()
        
    def get_btn(self):
        return self.confirm_btn


    def change_mode(self,mode):
        self.image_copy = self.image.copy()
        match mode:
            case "temperature":
                self.label.configure(text="Temperature")
                self.slider.configure(from_=-100, to=100, command=self.adjust_temperature)
                self.slider.set(0)
            case "brightness":
                self.label.configure(text="Brightness")
                self.slider.configure(from_=-100, to=100, command=self.adjust_brightness)
                self.slider.set(0)
            case "saturation":
                self.label.configure(text="Saturation")
                self.slider.configure(from_=0, to=2, command=self.adjust_saturation)
                self.slider.set(1)
            
            
    def adjust_temperature(self, kelvin_temp):
        kelvin_temp = self.slider.get() #self.temp_slider.get()

        if kelvin_temp == 0:
            self.image = self.image_copy.copy()
            self.update_image()
            return

        cold_tint = np.array([120, 128, 128], dtype=np.uint8)  # Cold tint (blue)
        warm_tint = np.array([30, 255, 255], dtype=np.uint8)   # Warm tint (orange)

        # Interpolate between cold and warm tint colors based on input value
        tint_color = cv2.addWeighted(cold_tint, (100 - kelvin_temp) / 100, warm_tint, kelvin_temp / 100, 0)

        # Convert tint color to BGR for overlaying on image
        tint_color_bgr = cv2.cvtColor(np.array([[tint_color]], dtype=np.uint8), cv2.COLOR_RGB2BGR)[0][0]

        # Apply the tint color as an overlay on the image
        tinted_image = cv2.addWeighted(self.image_copy.copy(), 1, np.zeros_like(self.image_copy.copy()), 0, 0)
        self.image = cv2.addWeighted(tinted_image, 1, np.full_like(self.image_copy.copy(), tint_color_bgr), 0.5, 0)


        # Convert the image back to RGB color space
        #self.image = cv2.cvtColor(tinted_image, cv2.COLOR_BGR2RGB)
        
        self.update_image()


    def adjust_brightness(self, brightness):
        brightness = self.slider.get() #self.brightness_slider.get()
        # Convert image to HSV color space
        hsv_image = cv2.cvtColor(self.image_copy.copy(), cv2.COLOR_RGB2HSV)
        
        # Add the brightness value to the V channel
        hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
        
        # Clip the values to ensure they are in the valid range [0, 255]
        hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
        hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
        
        # Convert the image back to BGR color space
        self.image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
        
        
        #self.brightness_value = int(value)
        self.update_image()
    
    def adjust_saturation(self,saturation_factor):
        saturation_factor = self.slider.get() #self.saturation_slider.get()
        # Convert image to HSV color space
        hsv_image = cv2.cvtColor(self.image_copy.copy(), cv2.COLOR_RGB2HSV)
        
        # Scale the saturation channel
        hsv_image[:, :, 1] = cv2.multiply(hsv_image[:, :, 1], saturation_factor)
        
        # Clip the values to ensure they are in the valid range [0, 255]
        hsv_image[:, :, 1] = cv2.add(hsv_image[:, :, 1], saturation_factor)
        hsv_image[:, :, 1] = cv2.add(hsv_image[:, :, 1], saturation_factor)
        
        # Convert the image back to BGR color space
        self.image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
        
        
        #self.saturation_value = float(value)
        self.update_image()
    
    def update_image(self):
        self.display_image = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(image=self.display_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

def open_popup(image):
    popup = tk.Toplevel()
    app = ImageAdjustmentPopup(popup, image)
    return app
