from utils import save_image

import numpy as np
import cv2
import keras

class Recognizer:

    @staticmethod
    def split_digits(img):
        """
        Slice the grid into 81 pieces to get images of each cell and prepare images for the model.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
        ret, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV) # Apply threshold
        
        # Slice the grid into 81 pieces to get images of each cell
        boxes = []
        rows = np.vsplit(thresh, 9)
        for row in rows:
            cols= np.hsplit(row, 9)
            for box in cols:
                box = box[3:47, 3:47] # DON'T CHANGE THESE VALUES! THE SOLUTION WON'T WORK FOR SOME REASON. I HATE THIS.
                boxes.append(box)

        # Center the digits
        for i, box in enumerate(boxes):
            contours, hier = cv2.findContours(box, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0: continue
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            blank = np.zeros((box.shape), np.uint8)

            if h / box.shape[1] < 0.15 or w / box.shape[0] < 0.15: 
                boxes[i] = blank
                continue

            yoff = (box.shape[1] - h) // 2
            xoff = (box.shape[0] - w) // 2
            blank[yoff:yoff+h, xoff:xoff+w] = box[y:y+h, x:x+w]
            boxes[i] = blank

        # Prepare images for the model
        digits = []
        for box in boxes:
            box = cv2.resize(box, (28, 28))
            box = np.reshape(box, (28, 28))
            box = box / 255
            digits.append(box)

        return np.array(digits)


    @staticmethod
    def recognize_digits(digits):
        """
        Predict the digits from splitted digit images.
        """
        model = keras.models.load_model("model.h5") # Load the model
        predictions = model.predict(digits) # Predict the digits from splitted digit images

        # Find the best prediction
        results = []
        for prediction in predictions:
            max = np.argmax(prediction) if np.max(prediction) > 0.5 else 0
            results.append(max)
        results = np.array(results).reshape((9, 9)) 
        
        # Create an image of recognized digits just for display purposes
        image_results = np.zeros((450, 450, 3), np.uint8)
        for y, row in enumerate(results):
            for x, digit in enumerate(row):
                if digit == 0: continue
                cv2.putText(image_results, str(digit), (x*50+10, y*50+40), cv2.FONT_HERSHEY_DUPLEX, 1.4, (255, 255, 255), lineType=cv2.LINE_AA)

        # Save the images for display purposes
        save_image(image_results, 23)

        return results