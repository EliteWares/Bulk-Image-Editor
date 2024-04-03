import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define a simple CNN model for facial blemish detection and removal
def create_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Load the pre-trained model for facial blemish detection
model = create_model(input_shape=(100, 100, 3))  # Assuming input images are resized to 100x100
model.load_weights('facial_blemish_detection_model.h5')  # Load pre-trained weights


# Function to detect and remove facial blemishes from an image
def remove_blemishes(image):
        # Perform facial blemish detection using the pre-trained model
        # You'll need to implement this part using face detection algorithms and then applying the model
        # For simplicity, I'll assume the image has already been preprocessed and faces are detected
        def detect_faces_in_images(images):
            faces_list = []
            for image in images:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                faces_list.append(faces)
            return faces_list

    # Function to apply facial blemish detection and removal on detected faces
        def process_faces(image, faces):
            for (x, y, w, h) in faces:
                face_roi = image[y:y+h, x:x+w]  # Extract the region of interest (face)
                # Preprocess the face image (resize, normalize, etc.) before feeding it to the model
                face_roi_resized = cv2.resize(face_roi, (100, 100))  # Resize face to model input size
                # Apply the pre-trained model for facial blemish detection
                # Replace this part with your actual facial blemish detection model
                # For demonstration, let's just blur the detected faces
                face_roi_processed = cv2.GaussianBlur(face_roi_resized, (15, 15), 0)
                # Replace the processed face back into the original image
                image[y:y+h, x:x+w] = face_roi_processed
            return image
        # Remove blemishes detected by the model
        # You can implement your own logic here based on the model predictions
        
        # For demonstration purposes, let's just blur the detected areas
        blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
        return blurred_image

    # Function to resize an image to specified dimensions
    def resize_image(image, width, height):
        return cv2.resize(image, (width, height))

# Example usage:
input_images = ("FolderInput.py")  # List of input images
faces_list = detect_faces_in_images(input_images)  # Detect faces in the images
output_images = process_faces(input_images, faces_list)  # Apply facial blemish detection and removal
input_image = cv2.imread('input_image.jpg')  # Load input image
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
input_image_resized = resize_image(input_image, 100, 100)  # Resize image to model input size
output_image = remove_blemishes(input_image_resized)  # Remove facial blemishes
output_image_resized = resize_image(output_image, input_image.shape[1], input_image.shape[0])  # Resize back to original size
cv2.imwrite('output_image.jpg', cv2.cvtColor(output_image_resized, cv2.COLOR_RGB2BGR))  # Save output image
 