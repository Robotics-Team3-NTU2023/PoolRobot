
# import the necessary packages
import cv2
import numpy as np

def img_preprocess(img):
    # Adjust the brightness and contrast 
    # Adjusts the brightness by subtracting 5 to each pixel value 
    brightness = -5 
    # Adjusts the contrast by scaling the pixel values by 1.3 
    contrast = 1.3
    res = cv2.addWeighted(img, contrast, np.zeros(img.shape, img.dtype), 0, brightness)
    cv2.imwrite("./proc_img.png",res)