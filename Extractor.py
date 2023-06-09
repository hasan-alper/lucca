from utils import save_image

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

        # Save the images for display purposes
        save_image(img, 1)
        save_image(gray, 2)
        save_image(blur, 3)

        return blur
    

    @staticmethod
    def detect_outerbox(img, dst):
        """
        Detects the outerbox of the puzzle by finding the largest contour. Then, applys a mask to get rid of the outer parts of the puzzle.
        """
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 12) # Convert image to binary before finding contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

        # Find the largest contour
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            approx = cv2.approxPolyDP(contour, 0.05*cv2.arcLength(contour, True), True)
            if area > max_area and len(approx)==4:
                max_area = area
                largest_contour = contour

        mask = np.zeros(img.shape, np.uint8) # Create a blank mask
        cv2.drawContours(mask, [largest_contour], 0, 255, -1) # Draw and fill up the largest contour we found
        masked = cv2.bitwise_and(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY), mask) # Apply the mask to the grayscale image

        # Save the images for display purposes
        save_image(thresh, 4)
        save_image(mask, 5)
        save_image(masked, 6)

        return masked
    

    @staticmethod
    def detect_grid(img):
        """
        Finds all the vertical and horizantal lines.
        """
        gradient_x = cv2.Sobel(img, cv2.CV_16S, 1, 0) # Find the all the vertical lines
        gradient_x = cv2.convertScaleAbs(gradient_x) # Convert to 8-bit, scale the values between 0-255
        blur_x = cv2.blur(gradient_x, (7, 25)) # Add some blur
        ret, thresh_x = cv2.threshold(blur_x, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Apply thresholding before finding contours
        contours, hierarchy = cv2.findContours(thresh_x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find all the contours

        # Find the contours whose ratio of height/width is greater than 6 to differentiate lines from numbers
        lines_x = thresh_x.copy()
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h / w > 6:
                cv2.drawContours(lines_x, [contour], 0, 255, -1)
            else:
                cv2.drawContours(lines_x, [contour], 0, 0, -1)
        
        final_x = cv2.blur(lines_x, (3, 125)) # Add some blur
        
        gradient_y = cv2.Sobel(img, cv2.CV_16S, 0, 1) # Find the all the horizontal lines
        gradient_y = cv2.convertScaleAbs(gradient_y) # Convert to 8-bit, scale the values between 0-255
        blur_y = cv2.blur(gradient_y, (25, 3)) # Add some blur
        ret, thresh_y = cv2.threshold(blur_y, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Apply thresholding before finding contours
        contours, hierarchy = cv2.findContours(thresh_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find all the contours
        
        # Find the contours whose ratio of width/height is greater than 6 to differentiate lines from numbers
        lines_y = thresh_y.copy()
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w / h > 6:
                cv2.drawContours(lines_y, [contour], 0, 255, -1)
            else:
                cv2.drawContours(lines_y, [contour], 0, 0, -1)

        final_y = cv2.blur(lines_y, (125, 3)) # Add some blur

        intersection = cv2.bitwise_and(final_x, final_y) # Find the intersection of the vertical and the horizantal lines
        ret, intersection = cv2.threshold(intersection, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Apply final thresholding
        dilate = cv2.morphologyEx(intersection, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)), 1) # Thicken the intersection points
        blur = cv2.blur(dilate, (10, 10)) # Smoothen the intersection points

        # Save the images for display purposes
        save_image(gradient_x, 7)
        save_image(blur_x, 8)
        save_image(thresh_x, 9)
        save_image(lines_x, 10)
        save_image(final_x, 11)
        save_image(gradient_y, 12)
        save_image(blur_y, 13)
        save_image(thresh_y, 14)
        save_image(lines_y, 15)
        save_image(final_y, 16)
        save_image(intersection, 17)
        save_image(dilate, 18)
        save_image(blur, 19)
        
        return blur


    @staticmethod
    def determine_vertices(img, dst):
        """
        Finds the centroid of the points where the lines intersect.
        """
        contours, hier = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Find the contours
        
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
        grid1 = dst.copy()
        for i, (x, y) in enumerate(centroids):
            cv2.circle(grid1, (x, y), 4, (0, 255, 0), -1)
            cv2.putText(grid1, str(i), (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 0))

        # Draw the centroids on the intersection image (Only for display purposes)
        grid2 = img.copy()
        grid2 = cv2.merge((grid2, grid2, grid2))
        for i, (x, y) in enumerate(centroids):
            cv2.circle(grid2, (x, y), 4, (0, 255, 0), -1)

        # Save the images for display purposes
        save_image(grid2, 20)
        save_image(grid1, 21)

        return centroids
    

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

        # Save the images for display purposes
        save_image(corrected, 22)

        return corrected