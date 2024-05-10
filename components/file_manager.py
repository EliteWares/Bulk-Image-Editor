import os
import cv2 as cv
from tkinter import filedialog

# Function to load images from a folder
def get_bgr_from_folder(folder_path):
    images = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if the file is a valid image file
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            # Read the image from file
            image = cv.imread(file_path)
            if image is not None:
                images.append(image)
            else:
                print(f"Unable to read image from file: {file_path}")
        else:
            print(f"Skipping non-image file: {file_path}")
    return images

def get_rgb_from_path(file_path):
    return cv.cvtColor(cv.imread(filename=file_path), cv.COLOR_BGR2RGB)

def get_bgr_from_path(file_path):
    return cv.imread(filename=file_path)

def get_bgr_from_rgb(img):
    return cv.cvtColor(img, cv.COLOR_RGB2BGR)

def get_rgb_from_bgr(img):
    return cv.cvtColor(img, cv.COLOR_BGR2RGB)

def save_image(img):
    save_path = filedialog.asksaveasfilename(title="Choose a save location",
    filetypes=[('image files', ('.png', '.jpg','.jpeg'))])

    if save_path:
        cv.imwrite(filename=save_path,img=get_bgr_from_rgb(img))

def save_images(imgs):
    save_path = filedialog.askdirectory(title="Choose export folder")
    if not save_path:
        return
    
    
    for i in range(len(imgs)):
        path = save_path + f"/test-export-{i}.png"
        cv.imwrite(filename=path,img=imgs[i])