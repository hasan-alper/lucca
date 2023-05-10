import os
import cv2
        
def save_image(img, i):
    """
    A utility function to save the image to specified directory.
    """
    cv2.imwrite(f"StageImages/{i}.jpg", img)