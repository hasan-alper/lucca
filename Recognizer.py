import numpy as np
import cv2
import keras

class Recognizer:

    def __init__(self, img):
        self.image = img # Load the image

    def split_digits(self):
        ret, thresh = cv2.threshold(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY_INV) # Apply threshold

        # Slice the grid into 81 pieces to get images of each cell
        boxes = []
        rows = np.vsplit(thresh, 9)
        for row in rows:
            cols= np.hsplit(row, 9)
            for box in cols:
                boxes.append(box)


        # Center the digits
        for i, box in enumerate(boxes):
            contours, hier = cv2.findContours(box, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0: continue
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            blank = np.zeros((box.shape), np.uint8)
            yoff = (box.shape[1] - h) // 2
            xoff = (box.shape[0] - w) // 2
            blank[yoff:yoff+h, xoff:xoff+w] = box[y:y+h, x:x+w]
            boxes[i] = blank

        # Prepare images for the model
        digits = []
        for box in boxes:
            box = box[3:47, 3:47]
            box = cv2.resize(box, (28, 28))
            box = np.reshape(box, (28, 28))
            box = box / 255
            digits.append(box)

        self.digits = np.array(digits)

    def recognize_digits(self):
        model = keras.models.load_model("model.h5") # Load the model
        predictions = model.predict(self.digits) # Predict the digits from splitted digit images

        # Find the best prediction
        results = []
        for prediction in predictions:
            max = np.argmax(prediction) if np.max(prediction) > 0.5 else 0
            results.append(max)

        results = np.array(results)

        print(results.reshape((9, 9)))