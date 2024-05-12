import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def draw_color_wheel(radius):
    # Create a blank image
    width = height = 2 * radius
    color_wheel = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw the color wheel
    for y in range(height):
        for x in range(width):
            angle = np.arctan2(y - radius, x - radius)
            hue = (angle + np.pi) / (2 * np.pi)
            saturation = np.sqrt((x - radius) ** 2 + (y - radius) ** 2) / radius
            if saturation <= 1:
                color = hsv_to_bgr(hue, saturation, 1.0)
                color_wheel[y, x] = color

    return color_wheel

def hsv_to_bgr(h, s, v):
    c = v * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = v - c
    if 0 <= h < 1 / 6:
        return int((c + m) * 255), int((x + m) * 255), int(m * 255)
    elif 1 / 6 <= h < 1 / 3:
        return int((x + m) * 255), int((c + m) * 255), int(m * 255)
    elif 1 / 3 <= h < 1 / 2:
        return int(m * 255), int((c + m) * 255), int((x + m) * 255)
    elif 1 / 2 <= h < 2 / 3:
        return int(m * 255), int((x + m) * 255), int((c + m) * 255)
    elif 2 / 3 <= h < 5 / 6:
        return int((x + m) * 255), int(m * 255), int((c + m) * 255)
    else:
        return int((c + m) * 255), int(m * 255), int((x + m) * 255)

def update_color(event):
    x, y = event.x, event.y
    if 0 <= x < color_wheel.shape[1] and 0 <= y < color_wheel.shape[0]:
        b, g, r = color_wheel[y, x]
        update_sliders(r, g, b)

def update_sliders(r, g, b):
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)

def update_color_from_sliders(event=None):
    r = r_slider.get()
    g = g_slider.get()
    b = b_slider.get()
    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    color_label.config(text="Selected Color: " + hex_color, bg=hex_color)

# Create a blank image and draw the color wheel
color_wheel = draw_color_wheel(radius=150)

# Initialize Tkinter window
root = tk.Tk()
root.title("Color Picker")

# Create a canvas to display the color wheel
canvas = tk.Canvas(root, width=color_wheel.shape[1], height=color_wheel.shape[0])
canvas.pack()

# Convert OpenCV image to Tkinter PhotoImage
color_wheel_img = cv2.cvtColor(color_wheel, cv2.COLOR_BGR2RGB)
color_wheel_img = ImageTk.PhotoImage(image=Image.fromarray(color_wheel_img))
canvas.create_image(0, 0, anchor=tk.NW, image=color_wheel_img)

# Label to display the selected color
color_label = tk.Label(root, text="Selected Color: ", font=("Arial", 12), pady=10)
color_label.pack()

# Create sliders for BGR values
r_slider = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
r_slider.pack()
g_slider = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
g_slider.pack()
b_slider = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
b_slider.pack()

# Bind mouse click event to update selected color and sliders
canvas.bind("<Button-1>", update_color)
r_slider.bind("<Motion>", update_color_from_sliders)
g_slider.bind("<Motion>", update_color_from_sliders)
b_slider.bind("<Motion>", update_color_from_sliders)

# Run the Tkinter event loop
root.mainloop()
