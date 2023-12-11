import cv2 
import numpy as np 

def detect_circle(img):

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
        param2 = 30, minRadius = 20, maxRadius = 50)
    
    # Draw circles that are detected. 
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2]
            # Draw the circumference of the circle. 
            # cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            # cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            return a, b
    
    return 0, 0
