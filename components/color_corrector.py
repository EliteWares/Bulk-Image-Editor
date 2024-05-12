import tkinter as tk
import numpy as np
from tkinter import ttk, Label, Button
import cv2
from PIL import Image, ImageTk


def apply_white_balance(image):
    # Convert the image to Lab color space
    lab_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2LAB)
    
    # Split the Lab image into its components
    L, a, b = cv2.split(lab_image)
    
    # Calculate the average values of the L, a, and b channels
    avg_L = np.mean(L)
    avg_a = np.mean(a)
    avg_b = np.mean(b)
    
    # Calculate the scaling factors for each channel
    L_scale = 128 / avg_L
    a_scale = 128 / avg_a
    b_scale = 128 / avg_b
    
    # Apply the scaling factors to each pixel in the image
    scaled_L = np.clip(L * L_scale, 0, 255).astype(np.uint8)
    scaled_a = np.clip(a * a_scale, 0, 255).astype(np.uint8)
    scaled_b = np.clip(b * b_scale, 0, 255).astype(np.uint8)
    
    # Merge the scaled channels back into Lab image
    balanced_lab_image = cv2.merge((scaled_L, scaled_a, scaled_b))
    
    # Convert the balanced Lab image back to BGR color space
    balanced_bgr_image = cv2.cvtColor(balanced_lab_image, cv2.COLOR_LAB2RGB)
    
    return balanced_bgr_image

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
'''
        cold_tint = np.array([120, 128, 128], dtype=np.uint8)  # Cold tint (blue)
        warm_tint = np.array([30, 255, 255], dtype=np.uint8)   # Warm tint (orange)

        # Interpolate between cold and warm tint colors based on input value
        tint_color = cv2.addWeighted(cold_tint, (100 - kelvin_temp) / 100, warm_tint, kelvin_temp / 100, 0)

        # Convert tint color to BGR for overlaying on image
        tint_color_bgr = cv2.cvtColor(np.array([[tint_color]], dtype=np.uint8), cv2.COLOR_RGB2BGR)[0][0]

        # Apply the tint color as an overlay on the image
        tinted_image = cv2.addWeighted(img.copy(),
                       1,
                       np.zeros_like(img.copy()),
                       0,
                       0)
        output = cv2.addWeighted(tinted_image,
                                       1,
                                       np.full_like(tinted_image,
                                       tint_color_bgr),
                                       0.5,
                                       0)
        return cv2.cvtColor(output, cv2.COLOR_HSV2RGB)
'''        

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
        self.label.pack()

        self.slider = ttk.Scale(self.master,
                                from_=-25,
                                to=25,
                                orient=tk.HORIZONTAL,
                                command=self.adjust_temp)
        self.slider.pack(fill=tk.X)
        self.slider
        self.slider.set(0)

        self.temp_btn = Button(self.master,
                               text="Temperature",
                               command=lambda: self.change_mode("temperature"))
        self.temp_btn.pack()

        self.bright_btn = Button(self.master,
                               text="Brightness",
                               command=lambda: self.change_mode("brightness"))
        self.bright_btn.pack()

        self.contr_btn = Button(self.master,
                               text="Contrast",
                               command=lambda: self.change_mode("contrast"))
        self.contr_btn.pack()
        
        self.highlight_btn = Button(self.master,
                               text="Highlights",
                               command=lambda: self.change_mode("highlights"))
        self.highlight_btn.pack()

        self.shadow_btn = Button(self.master,
                               text="Shadows",
                               command=lambda: self.change_mode("shadows"))
        self.shadow_btn.pack()

        self.sat_btn = Button(self.master,
                               text="Saturation",
                               command=lambda: self.change_mode("saturation"))
        self.sat_btn.pack()

        self.white_bal_btn = Button(self.master,
                               text="Apply White Balance",
                               command= self.white_balance)
        self.white_bal_btn.pack()

        self.confirm_btn = Button(self.master,
                               text="Confirm",
                               command=lambda: print("Confirm"))
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
        kelvin_temp = self.slider.get() #self.temp_slider.get()

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

    def white_balance(self):
        if self.is_command: self.commands.append(["White Balance"])

        self.image = apply_white_balance(self.image_copy)
        
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
