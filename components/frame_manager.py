import cv2

def overlay(base_img,overlay_img):
    # Read base image and overlay image
    # Get dimensions of base image
    base_img_copy = cv2.imread(base_img)
    overlay_copy = cv2.imread(overlay_img,cv2.IMREAD_UNCHANGED)
    height, width, _ = base_img_copy.shape

    # Resize overlay image to match dimensions of base image
    overlay_img_resized = cv2.resize(overlay_copy, (width, height))

    # Overlay resized image onto base image
    for y in range(height):
        for x in range(width):
            alpha = overlay_img_resized[y, x, 3] / 255.0  # Alpha channel
            base_img_copy[y, x] = alpha * overlay_img_resized[y, x, 0:3] + (1 - alpha) * base_img_copy[y, x]

    cv2.imshow("Overlay Image", base_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return base_img_copy      
    
