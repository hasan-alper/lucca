import cv2
import numpy as np
import matplotlib.pyplot as plt

############################
#  PREPROCESSING THE IMAGE #
############################

img = cv2.imread("images/sudoku-1.png")  # Import the image
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 10) # Add some blur to reduce noise and details

###########################
#  FIND THE SUDOKU SQUARE #
###########################

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

mask = np.zeros((img_gray.shape), np.uint8) # Create a blank mask
cv2.drawContours(mask, [largest_contour], 0, 255, -1) # Draw and fill up the largest contour we found
img_masked = cv2.bitwise_and(img_gray, mask) # Apply the mask to the grayscale image

###############################
#  FINDING THE VERTICAL LINES #
###############################

gradient_x = cv2.Sobel(img_masked, cv2.CV_16S, 1, 0) # Find the all vertical lines
gradient_x = cv2.convertScaleAbs(gradient_x) # Convert to 8-bit since Otsu Threshold only works with 8-bit single-channel images
ret, thresh_x = cv2.threshold(gradient_x, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Apply thresholding before finding contours
close_x = cv2.morphologyEx(thresh_x, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 10)), 1) # Fill out any cracks in the board lines
contours, hierarchy = cv2.findContours(close_x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

# Find the contours whose ratio of height/width is greater than 5 to differentiate lines from numbers
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if h / w > 5:
        cv2.drawContours(close_x, [contour], 0, 255, -1)
    else:
        cv2.drawContours(close_x, [contour], 0, 0, -1)

#################################
#  FINDING THE HORIZANTAL LINES #
#################################

gradient_y = cv2.Sobel(img_masked, cv2.CV_16S, 0, 1) # Find the all horizontal lines
gradient_y = cv2.convertScaleAbs(gradient_y) # Convert to 8-bit since Otsu Threshold only works with 8-bit single-channel images
ret, thresh_y = cv2.threshold(gradient_y, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Apply thresholding before finding contours, again
close_y = cv2.morphologyEx(thresh_y, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2)), 1) # Fill out any cracks in the board lines
contours, hierarchy = cv2.findContours(close_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

# Find the contours whose ratio of width/height is greater than 5 to differentiate lines from numbers
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w / h > 5:
        cv2.drawContours(close_y, [contour], 0, 255, -1)
    else:
        cv2.drawContours(close_y, [contour], 0, 0, -1)

############################
#  FINDING THE GRID POINTS #
############################

intersection = cv2.bitwise_and(close_x, close_y) # Find the intersection of the vertical and the horizantal lines
close = cv2.morphologyEx(intersection, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)), 1) # Thicken the intersection points
contours, hier = cv2.findContours(close, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Find the contours

# Find the centroids
centroids = []
for contour in contours:
    mom = cv2.moments(contour)
    try: (x, y) = int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"])
    except: pass
    centroids.append((x, y))

# Sort them from left to right, top to bottom
centroids = np.array(centroids)
centroids = centroids[np.argsort(centroids[:, 1])]
centroids = np.vstack([centroids[i*10:(i+1)*10][np.argsort(centroids[i*10:(i+1)*10,0])] for i in range(10)])

# Draw the centroids on the original image
for i, (x, y) in enumerate(centroids):
    cv2.circle(img, (x, y), 4, (0, 255, 0), -1)
    cv2.putText(img, str(i), (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0))

plt.imshow(img)

plt.show()