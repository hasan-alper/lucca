import numpy as np
import cv2

class Extractor:

    @staticmethod
    def preprocess_image(img):
        """
        Converts the image to grayscale and adds blur to reduce noise and details.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
        blur = cv2.GaussianBlur(gray, (5, 5), 10) # Add blur

        return blur
    

    @staticmethod
    def detect_outerbox(img, dst):
        """
        Detects the outerbox of the puzzle by finding the largest contour. Then, applys a mask to get rid of the outer parts of the puzzle.
        """
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 8) # Convert image to binary before finding contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

        # Find the largest contour
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        mask = np.zeros(img.shape, np.uint8) # Create a blank mask
        cv2.drawContours(mask, [largest_contour], 0, 255, -1) # Draw and fill up the largest contour we found
        masked = cv2.bitwise_and(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY), mask) # Apply the mask to the grayscale image
        return masked
    

    @staticmethod
    def detect_grid(img):
        """
        Finds all the vertical and horizantal lines.
        """
        gradient_x = cv2.Sobel(img, cv2.CV_16S, 1, 0) # Find the all vertical lines
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
 
        gradient_y = cv2.Sobel(img, cv2.CV_16S, 0, 1) # Find the all horizontal lines
        gradient_y = cv2.convertScaleAbs(gradient_y) # Convert to 8-bit since Otsu Threshold only works with 8-bit single-channel images
        ret, thresh_y = cv2.threshold(gradient_y, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Apply thresholding before finding contours, again
        close_y = cv2.morphologyEx(thresh_y, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2)), 1) # Fill out any cracks in the board lines
        contours, hierarchy = cv2.findContours(close_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find all the contours

        # Find the contours whose ratio of width/height is greater than 5 to differentiate lines from numbers
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w / h > 5:
                cv2.drawContours(close_y, [contour], 0, 255, -1)
            else:
                cv2.drawContours(close_y, [contour], 0, 0, -1)

        intersection = cv2.bitwise_and(close_x, close_y) # Find the intersection of the vertical and the horizantal lines

        return intersection


    @staticmethod
    def determine_vertices(img, dst):
        """
        Finds the centroid of the points where the lines intersect.
        """
        close = cv2.morphologyEx(img, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)), 1) # Thicken the intersection points
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

        # Draw the centroids on the destination image
        grid = dst.copy()
        for i, (x, y) in enumerate(centroids):
            cv2.circle(grid, (x, y), 6, (0, 255, 0), -1)
            cv2.putText(grid, str(i), (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 0))

        return centroids, grid
    

    @staticmethod
    def correct_perspective(centroids, dst):
        """
        Applies a perspective transform based on found centroids.
        """
        corrected = np.zeros((450, 450, 3), np.uint8) # Create a blank image.
        for i in range(100):
            r = i // 10
            c = i % 10

            if c == 9 or r == 9: continue

            source = np.array([centroids[i], centroids[i+1], centroids[i+10], centroids[i+11]], dtype=np.float32) # Get the vertices of each cell in the source image
            destination = np.array([[50*c, 50*r], [50*c+50, 50*r], [50*c, 50*r+50], [50*c+50, 50*r+50]], dtype=np.float32)  # Calculate correspording cells
            mat = cv2.getPerspectiveTransform(source, destination) # Get the transformation matrix
            warp = cv2.warpPerspective(dst, mat, (450, 450)) # Apply the transformation to destination image.
            corrected[50*r:50*r+50, 50*c:50*c+50] = warp[50*r:50*r+50, 50*c:50*c+50] # Build the final image one cell at a time

        return corrected