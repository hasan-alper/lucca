import numpy as np
import cv2
import os

class Extractor:

    def __init__(self, path):
        self.image = cv2.imread(path) # Load the image
        self.original = cv2.imread(path)
        self._write_images(self.image, 1)

    def preprocess_image(self):
        self.image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
        self._write_images(self.image_gray, 2)
        image_blur = cv2.GaussianBlur(self.image_gray, (5, 5), 10) # Add blur to reduce noise and details
        self._write_images(image_blur, 3)
        self.image = image_blur

    def detect_grid(self):
        image_thresh = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 8) # Convert image to binary before finding contours for better accuracy
        self._write_images(image_thresh, 4)
        contours, hierarchy = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

        # Find the largest contour
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        mask = np.zeros((self.image.shape), np.uint8) # Create a blank mask
        cv2.drawContours(mask, [largest_contour], 0, 255, -1) # Draw and fill up the largest contour we found
        image_masked = cv2.bitwise_and(self.image_gray, mask) # Apply the mask to the grayscale image
        self._write_images(image_masked, 5)
        self.image = image_masked

    def detect_lines(self):
        gradient_x = cv2.Sobel(self.image, cv2.CV_16S, 1, 0) # Find the all vertical lines
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
 
        gradient_y = cv2.Sobel(self.image, cv2.CV_16S, 0, 1) # Find the all horizontal lines
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

        image_intersection = cv2.bitwise_and(close_x, close_y) # Find the intersection of the vertical and the horizantal lines
        image_grid = cv2.bitwise_or(close_x, close_y)
        self._write_images(image_grid, 6)
        self.image = image_intersection

    def detect_vertices(self):
        close = cv2.morphologyEx(self.image, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)), 1) # Thicken the intersection points
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
        grid = self.original.copy()
        for i, (x, y) in enumerate(centroids):
            cv2.circle(grid, (x, y), 6, (0, 255, 0), -1)
            cv2.putText(grid, str(i), (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 0))

        self._write_images(grid, 7)
        self.centroids = centroids

    def correct_perspective(self):
        # Apply transform
        corrected = np.zeros((450, 450, 3), np.uint8)
        for i in range(100):
            r = i // 10
            c = i % 10

            if c == 9 or r == 9: continue

            src = np.array([self.centroids[i], self.centroids[i+1], self.centroids[i+10], self.centroids[i+11]], dtype=np.float32)
            dst = np.array([[50*c, 50*r], [50*c+50, 50*r], [50*c, 50*r+50], [50*c+50, 50*r+50]], dtype=np.float32)
            mat = cv2.getPerspectiveTransform(src, dst)
            warp = cv2.warpPerspective(self.original, mat, (450, 450))
            corrected[50*r:50*r+50, 50*c:50*c+50] = warp[50*r:50*r+50, 50*c:50*c+50]

        self._write_images(corrected, 8)
        self.image = corrected

    def _write_images(self, img, i):
        try: os.remove(f"StageImages/{i}.jpg")
        except: pass
        cv2.imwrite(f"StageImages/{i}.jpg", img)