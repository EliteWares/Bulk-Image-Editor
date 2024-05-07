import cv2 as cv


def detect_face(file_path):
    image = cv.imread(file_path)
    gs = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    fc = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    faces = fc.detectMultiScale(gs,scaleFactor=1.1, minNeighbors=10)
    max_area = 0
    
    for (x,y,w,h) in faces:
        area = abs(w-x) * abs(h-y)
        if area > max_area:
            max_area = area
            face = [x,y,w,h]
        #draw_squares(image,[x,y,w,h])
    
    return image, face


def draw_squares(img, face):
    cv.rectangle(img, (face[0],face[1]), (face[0]+face[2], face[1]+face[3]),(255,0,0), 5)
    #resize_img = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)
    
    cv.imshow("Face Detection",img)
    

def apply_face_smoothing(image, face):
    # Extract face region
    x, y, w, h = face
    face_region = image[y:y+h, x:x+w]
    
    # Apply smoothing filter to face region
    smoothed_face = cv.bilateralFilter(face_region, 25, 50, 75)
    
    # Replace original face region with smoothed face
    image[y:y+h, x:x+w] = smoothed_face
    
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)

'''# Example usage
file_path = "imgs/acne-test2.webp"
image, face = detect_face(file_path)
smoothed_image = apply_face_smoothing(image, face)
cv.imshow("Smoothed Image", smoothed_image)
cv.waitKey(0)
cv.destroyAllWindows()'''