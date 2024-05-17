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
    img = img.astype(np.float32)
    
    # Calculate the mean of the image for per-channel adjustment
    mean = np.mean(img, axis=(0, 1), keepdims=True)
    
    # Adjust the contrast
    adjusted_img = contrast * (img - mean) + mean
    
    # Clip the values to stay within [0, 255]
    adjusted_img = np.clip(adjusted_img, 0, 255)
    
    # Convert back to uint8
    adjusted_img = adjusted_img.astype(np.uint8)
    
    return adjusted_img
    


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

