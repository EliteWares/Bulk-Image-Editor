import cv2 as cv

folder_path = "imgs/res/"


for i in range(1,8):
    filen= f"button_{i}.png"
    new_filen = f"button_{i}_hover.png"
    
    img = cv.imread(filename=folder_path+filen)
    h, w, _ = img.shape
    h,w = int(h*1.1),int(w*1.1)

    resized_img = cv.resize(img,(w,h))

    cv.imwrite(filename=folder_path+new_filen,img=resized_img)

