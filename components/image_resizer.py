import cv2 as cv
from tkinter import filedialog

def resize_image(img, dimensions):
    return cv.cvtColor(cv.resize(img, dimensions, interpolation=cv.INTER_AREA), cv.COLOR_BGR2RGB)

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