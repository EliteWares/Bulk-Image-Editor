import cv2 as cv


def detect_face(image):
    gs = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    fc = cv.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    
    faces = fc.detectMultiScale(gs,scaleFactor=1.1, minNeighbors=10)
    max_area = 0
    face = [0,0,0,0]
    
    for (x,y,w,h) in faces:
        area = abs(w-x) * abs(h-y)
        if area > max_area:
            max_area = area
            face = [x,y,w,h]
            
    return image, face

   

def apply_face_smoothing(image, face):
    # Extract face region
    x, y, w, h = face
    face_region = image[y:y+h, x:x+w]
    
    # Apply smoothing filter to face region
    smoothed_face = cv.bilateralFilter(face_region, 25, 50, 75)
    
    # Replace original face region with smoothed face
    image[y:y+h, x:x+w] = smoothed_face
    return image
    #return cv.cvtColor(image, cv.COLOR_BGR2RGB)


