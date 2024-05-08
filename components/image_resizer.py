import cv2 as cv
from tkinter import filedialog

def resize_image(img, dimensions):
    return cv.cvtColor(cv.resize(img, dimensions, interpolation=cv.INTER_AREA), cv.COLOR_BGR2RGB)

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

def get_rgb_from_path(file_path):
    return cv.cvtColor(cv.imread(filename=file_path), cv.COLOR_BGR2RGB)

def get_bgr_from_path(file_path):
    return cv.imread(filename=file_path)

def get_bgr_from_rgb(img):
    return cv.cvtColor(img, cv.COLOR_RGB2BGR)

def get_rgb_from_bgr(img):
    return cv.cvtColor(img, cv.COLOR_BGR2RGB)

def save(img):
    save_path = filedialog.asksaveasfilename(title="Choose a save location",
    filetypes=[('image files', ('.png', '.jpg','.jpeg'))])

    cv.imwrite(filename=save_path,img=get_bgr_from_rgb(img))