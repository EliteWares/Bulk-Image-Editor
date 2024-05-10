import cv2 as cv
from tkinter import filedialog

def resize_image(img, dimensions):
    return cv.resize(img, dimensions, interpolation=cv.INTER_AREA)

def resize_to_preview(image):
    # Get dimensions of the input image
    height, width = image.shape[:2]

    # Calculate aspect ratio
    aspect_ratio = width / height

    # Define maximum dimensions
    max_width = 544
    max_height = 544

    # Resize image while maintaining aspect ratio
    if width != max_width or height != max_height:
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)

        # Perform resizing
        resized_image = cv.resize(image, (new_width, new_height))
    else:
        # Image already fits within constraints
        resized_image = image

    return resized_image

