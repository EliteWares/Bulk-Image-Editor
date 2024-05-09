import tkinter as tk
from tkinter import ttk, Label
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageAdjustmentPopup:
    def __init__(self, master, image):
        self.master = master
        self.master.title("Image Adjustment")
        
        self.image = image
        self.original_image = self.image.copy()
        self.display_image = self.image
        
        self.width, self.height, _ = self.image.shape
        
        self.brightness_value = 0
        self.saturation_value = 1.0
        
        self.create_widgets()
        self.update_image()
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        
        self.image_tk = ImageTk.PhotoImage(Image.fromarray(self.display_image))
        self.canvas.create_image(0, 10, anchor=tk.NW, image=self.image_tk)
        
        self.brightness_label = Label(self.master,text="Brightness")
        self.brightness_label.pack()

        self.brightness_slider = ttk.Scale(self.master, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.pack(fill=tk.X)
        self.brightness_slider
        self.brightness_slider.set(0)
        
        self.saturation_label = Label(self.master,text="Saturation")
        self.saturation_label.pack()

        self.saturation_slider = ttk.Scale(self.master, from_=0, to=2, orient=tk.HORIZONTAL, command=self.update_saturation)
        self.saturation_slider.pack(fill=tk.X)
        self.saturation_slider.set(1.0)
    
    def update_brightness(self, brightness):
        brightness = self.brightness_slider.get()
        # Convert image to HSV color space
        hsv_image = cv2.cvtColor(self.original_image.copy(), cv2.COLOR_RGB2HSV)
        
        # Add the brightness value to the V channel
        hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
        
        # Clip the values to ensure they are in the valid range [0, 255]
        hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
        hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
        
        # Convert the image back to BGR color space
        self.image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
        
        
        #self.brightness_value = int(value)
        self.update_image()
    
    def update_saturation(self,saturation_factor):
        saturation_factor = self.saturation_slider.get()
        # Convert image to HSV color space
        hsv_image = cv2.cvtColor(self.original_image.copy(), cv2.COLOR_RGB2HSV)
        
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
