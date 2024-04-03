import os
import cv2

# Function to load images from a folder
def FolderInput(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if the file is a valid image file
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp']):
            # Read the image from file
            image = cv2.imread(file_path)
            if image is not None:
                images.append(image)
            else:
                print(f"Unable to read image from file: {file_path}")
        else:
            print(f"Skipping non-image file: {file_path}")
    return images

# Example usage:



folder_path = './ImageFolder'  # Path to the folder containing input images
input_images = FolderInput(folder_path)  # Load images from the folder
