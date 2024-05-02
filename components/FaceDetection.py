import numpy as np
import cv2 as cv
import os
    

def detect_face(file_path):
    image = cv.imread(file_path)
    gs = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    fc = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
    
    faces = fc.detectMultiScale(gs,scaleFactor=1.1, minNeighbors=10)
    max_area = 0
    
    
    if len(faces) > 1:
        #face = None
        for (x,y,w,h) in faces:
            area = abs(w-x) * abs(h-y)
            if area > max_area:
                max_area = area
                face = [x,y,w,h]
            draw_squares(image,[x,y,w,h])
        #draw_squares(image,face)

    else:
        print("one face")
        draw_squares(image,faces[0])
    
    

def get_img_shapes(path,batch_size):
    images = []
    folder = os.listdir(path)

    for filename in folder[:batch_size]:
        file_path = os.path.join(path, filename)
        # Check if the file is a valid image file
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp']):
            # Read the image from file
            image = cv.imread(file_path)
            if image is not None:
                images.append(image)
            else:
                print(f"Unable to read image from file: {file_path}")
        else:
            print(f"Skipping non-image file: {file_path}")
    return images


def draw_squares(img, face):
    cv.rectangle(img, (face[0],face[1]), (face[0]+face[2], face[1]+face[3]),(255,0,0), 5)
    
    resize_img = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)
    cv.imshow("Face Detection",resize_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def display_image(img):
    pass

        
