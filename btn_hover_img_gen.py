import cv2
import numpy as np
from tkinter import filedialog

folder_path = "imgs/res/"

def generate():
    for i in range(1,8):
        filen= f"button_{i}.png"
        new_filen = f"button_{i}_hover.png"
        
        img = cv2.imread(filename=folder_path+filen)
        h, w, _ = img.shape
        h,w = int(h*1.1),int(w*1.1)

        resized_img = cv2.resize(img,(w,h))

        cv2.imwrite(filename=folder_path+new_filen,img=resized_img)


def gray_world_algorithm(image):
    # Convert the image to Lab color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the Lab image into its components
    L, a, b = cv2.split(lab_image)
    
    # Calculate the average values of the L, a, and b channels
    avg_L = np.mean(L)
    avg_a = np.mean(a)
    avg_b = np.mean(b)
    
    # Calculate the scaling factors for each channel
    L_scale = 128 / avg_L
    a_scale = 128 / avg_a
    b_scale = 128 / avg_b
    
    # Apply the scaling factors to each pixel in the image
    scaled_L = np.clip(L * L_scale, 0, 255).astype(np.uint8)
    scaled_a = np.clip(a * a_scale, 0, 255).astype(np.uint8)
    scaled_b = np.clip(b * b_scale, 0, 255).astype(np.uint8)
    
    # Merge the scaled channels back into Lab image
    balanced_lab_image = cv2.merge((scaled_L, scaled_a, scaled_b))
    
    # Convert the balanced Lab image back to BGR color space
    balanced_bgr_image = cv2.cvtColor(balanced_lab_image, cv2.COLOR_LAB2BGR)
    
    return balanced_bgr_image



def apply_white_balance(image, lighting_condition):
    if lighting_condition not in ['tungsten', 'fluorescent', 'cloudy', 'shade']:
        raise ValueError("Invalid lighting condition. Supported options are 'tungsten', 'fluorescent', 'cloudy', and 'shade'.")

    # Define presets for each lighting condition
    presets = {
        'tungsten': {'b': 0.2, 'g': 0.4, 'r': 0.6},
        'fluorescent': {'b': 0.3, 'g': 0.7, 'r': 0.9},
        'cloudy': {'b': 0.8, 'g': 1.0, 'r': 1.2},
        'shade': {'b': 0.9, 'g': 1.0, 'r': 1.1}
    }

    # Apply color modifications based on the selected lighting condition
    modified_image = np.zeros_like(image)
    modified_image[:, :, 0] = np.clip(image[:, :, 0] * presets[lighting_condition]['b'], 0, 255).astype(np.uint8)
    modified_image[:, :, 1] = np.clip(image[:, :, 1] * presets[lighting_condition]['g'], 0, 255).astype(np.uint8)
    modified_image[:, :, 2] = np.clip(image[:, :, 2] * presets[lighting_condition]['r'], 0, 255).astype(np.uint8)

    return modified_image


file = filedialog.askopenfilename()
img = cv2.imread(filename=file)

wb_Type = "tungsten"


gray_World_img = gray_world_algorithm(img.copy())
custom_wb_img = apply_white_balance(img.copy(),wb_Type)

cv2.namedWindow("Original")
cv2.imshow(winname="Original",mat=img)

cv2.namedWindow("Gray World Algo")
cv2.imshow(winname="Gray World Algo",mat=gray_World_img)
cv2.namedWindow(wb_Type)
cv2.imshow(winname=wb_Type,mat=custom_wb_img)
cv2.waitKey(0)
cv2.destroyAllWindows()