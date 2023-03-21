import cv2
import matplotlib.pyplot as plt

############################
#  PREPROCESSING THE IMAGE #
############################

img = cv2.imread("images/sudoku.png")  # Import the image
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 10) # Add some blur to reduce noise and details

plt.imshow(img_blur, cmap="gray")
plt.show()
