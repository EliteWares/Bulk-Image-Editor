import tkinter as tk
import numpy as np
from tkinter import ttk, Label, Button
import cv2
from PIL import Image, ImageTk


def adjust_temperature(temp,img):
        if temp == 0: return img

        #return img
        # Define the color channels shift based on the temperature value
        blue_shift = 10 * temp
        red_shift = -10 * temp

        # Split the image into its color channels
        b, g, r = cv2.split(img.copy())

        # Apply the color channels shift
        b_adjusted = np.clip(b + blue_shift, 0, 255).astype(np.uint8)
        r_adjusted = np.clip(r + red_shift, 0, 255).astype(np.uint8)

        # Merge the adjusted channels
        adjusted_image = cv2.merge((b_adjusted, g, r_adjusted))

        return adjusted_image
   

def adjust_brightness(brightness,img):
    if brightness == 0: return img
    hsv_image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2HSV)
    
    # Add the brightness value to the V channel
    hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
    
    # Clip the values to ensure they are in the valid range [0, 255]
    hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
    hsv_image[:, :, 2] = cv2.add(hsv_image[:, :, 2], brightness)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

def adjust_contrast(contrast, img):
    if contrast == 0: return img
    # Convert contrast value to a scaling factor
    contrast_factor = (100 + contrast) / 100.0

    # Convert image to grayscale if it's not already
    if len(img.shape) == 3:
        gray_image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
    else:
        gray_image = img

    # Adjust contrast
    adjusted_image = cv2.convertScaleAbs(gray_image, alpha=contrast_factor, beta=0)

    return cv2.cvtColor(adjusted_image, cv2.COLOR_GRAY2RGB)


def adjust_highlights(highlight, img):
    # Convert image to LAB color space
    lab_image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2LAB)

    # Split LAB channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Normalize L channel to 0-1 range
    l_channel_normalized = l_channel / 255.0

    # Apply highlight adjustment
    adjusted_l_channel = np.clip(l_channel_normalized + (highlight / 100.0), 0, 1)

    # Scale back to 0-255 range
    adjusted_l_channel = (adjusted_l_channel * 255).astype(np.uint8)

    # Merge channels
    adjusted_lab_image = cv2.merge((adjusted_l_channel, a_channel, b_channel))

    # Convert back to RGB color space
    adjusted_image = cv2.cvtColor(adjusted_lab_image, cv2.COLOR_LAB2RGB)

    return adjusted_image

def adjust_shadows(shadow, img):
    # Convert image to LAB color space
    lab_image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2LAB)

    # Split LAB channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Normalize L channel to 0-1 range
    l_channel_normalized = l_channel / 255.0

    # Apply shadow adjustment
    adjusted_l_channel = np.clip(l_channel_normalized - (shadow / 100.0), 0, 1)

    # Scale back to 0-255 range
    adjusted_l_channel = (adjusted_l_channel * 255).astype(np.uint8)

    # Merge channels
    adjusted_lab_image = cv2.merge((adjusted_l_channel, a_channel, b_channel))

    # Convert back to RGB color space
    adjusted_image = cv2.cvtColor(adjusted_lab_image, cv2.COLOR_LAB2RGB)

    return adjusted_image


def adjust_saturation(saturation,img):
    if saturation == 1: return img
    hsv_image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2HSV)
    
    # Scale the saturation channel
    hsv_image[:, :, 1] = cv2.multiply(hsv_image[:, :, 1], saturation)
    
    # Clip the values to ensure they are in the valid range [0, 255]
    hsv_image[:, :, 1] = cv2.add(hsv_image[:, :, 1], saturation)
    hsv_image[:, :, 1] = cv2.add(hsv_image[:, :, 1], saturation)

    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)



class ImageAdjustmentPopup:
    def __init__(self, master, image, command):
        self.master = master
        self.master.title("Image Adjustment")

        self.is_command = command
        self.commands = []
        
        self.image = image
        self.image_copy = self.image.copy()
        self.original_image = self.image.copy()
        self.display_image = self.image
        
        self.width, self.height, _ = self.image.shape
        
        self.brightness_value = 0
        self.saturation_value = 1.0

        self.confirm_btn = Button(self.master,
                                  text="Confirm",
                                  command=lambda: print("Confirm"))
        
        self.create_widgets()
        self.update_image()

            
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        
        self.image_tk = ImageTk.PhotoImage(Image.fromarray(self.display_image))
        self.canvas.create_image(0, 10, anchor=tk.NW, image=self.image_tk)
        
        self.label = Label(self.master,text="Temperature")
        

        self.slider = ttk.Scale(self.master,
                                from_=-25,
                                to=25,
                                orient=tk.HORIZONTAL,
                                command=self.adjust_temp,
                                value=0)
                

        self.temp_btn = Button(self.master,
                               text="Temperature",
                               command=lambda: self.change_mode("temperature"))
        

        self.bright_btn = Button(self.master,
                               text="Brightness",
                               command=lambda: self.change_mode("brightness"))
        

        self.contr_btn = Button(self.master,
                               text="Contrast",
                               command=lambda: self.change_mode("contrast"))
        
        
        self.highlight_btn = Button(self.master,
                               text="Highlights",
                               command=lambda: self.change_mode("highlights"))
        

        self.shadow_btn = Button(self.master,
                               text="Shadows",
                               command=lambda: self.change_mode("shadows"))
        

        self.sat_btn = Button(self.master,
                               text="Saturation",
                               command=lambda: self.change_mode("saturation"))
        
        
        self.confirm_btn = Button(self.master,
                               text="Confirm",
                               command=lambda: print("Confirm"))
        
        self.label.pack()
        self.slider.pack(fill=tk.X)
        self.temp_btn.pack()
        self.bright_btn.pack()
        self.contr_btn.pack()
        self.highlight_btn.pack()
        self.shadow_btn.pack()
        self.sat_btn.pack()
        self.confirm_btn.pack()
        

    def change_mode(self,mode):
        if self.is_command:
            self.commands.append([self.label.cget("text"),self.slider.get()])
        
        
        self.image_copy = self.image.copy()
        
        match mode:
            case "temperature":
                
                self.label.configure(text="Temperature")
                self.slider.configure(from_=-25, to=25, command=self.adjust_temp)
                self.slider.set(0)
            case "brightness":
                self.label.configure(text="Brightness")
                self.slider.configure(from_=-100, to=100, command=self.adjust_bright)
                self.slider.set(0)
            case "contrast":
                self.label.configure(text="Contrast")
                self.slider.configure(from_=-100, to=100, command=self.adjust_contr)
                self.slider.set(0)
            case "saturation":
                self.label.configure(text="Saturation")
                self.slider.configure(from_=0, to=2, command=self.adjust_satur)
                self.slider.set(1)
            case "highlights":
                self.label.configure(text="Highlights")
                self.slider.configure(from_=-100, to=100, command=self.adjust_highlight)
                self.slider.set(0)
            case "shadows":
                self.label.configure(text="Shadows")
                self.slider.configure(from_=-100, to=100, command=self.adjust_shadow)
                self.slider.set(0)
            
            
    def adjust_temp(self, kelvin_temp):
        kelvin_temp = self.slider.get() 

        if kelvin_temp == 0:
            self.image = self.image_copy.copy()
            self.update_image()
            return
        
        self.image = adjust_temperature(temp=kelvin_temp,img=self.image_copy)
        
        self.update_image()


    def adjust_bright(self, brightness):
        brightness = self.slider.get()
        
        self.image = adjust_brightness(brightness,self.image_copy)
        
        self.update_image()
    
    def adjust_contr(self, contrast):
        contrast = self.slider.get()
        
        self.image = adjust_brightness(contrast,self.image_copy)
        
        self.update_image()
    
    def adjust_highlight(self, higlights):
        higlights = self.slider.get()
        
        self.image = adjust_highlights(higlights,self.image_copy)
        
        self.update_image()
    
    def adjust_shadow(self, shadows):
        shadows = self.slider.get()
        
        self.image = adjust_brightness(shadows,self.image_copy)
        
        self.update_image()

        
    def adjust_satur(self,saturation_factor):
        saturation_factor = self.slider.get() #self.saturation_slider.get()
        # Convert image to HSV color space
        
        
        # Convert the image back to BGR color space
        self.image = adjust_saturation(saturation_factor,self.image_copy)
        
        
        #self.saturation_value = float(value)
        self.update_image()
    
    def update_image(self):
        self.display_image = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(image=self.display_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

def open_popup(image, command):
    popup = tk.Toplevel()
    app = ImageAdjustmentPopup(popup, image, command)
    return app
