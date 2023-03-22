import cv2
import numpy as np
import matplotlib.pyplot as plt

############################
#  PREPROCESSING THE IMAGE #
############################

img = cv2.imread("images/sudoku.png")  # Import the image
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 10) # Add some blur to reduce noise and details

#######################
#  FIND SUDOKU SQUARE #
#######################

img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 8) # Convert image to binary before finding contours for better accuracy
contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

# Find the largest contour
max_area = 0
largest_contour = None
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        largest_contour = contour

# Create masked image
mask = np.zeros((img.shape), np.uint8)
cv2.drawContours(mask, [largest_contour], 0, (255, 255, 255), -1)
img_masked = cv2.bitwise_and(img, mask)


plt.imshow(img_masked)

plt.show()
