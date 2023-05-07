import cv2
import os

from Extractor import Extractor
from Recognizer import Recognizer
from Solver import Solver

class Sudoku:

    def __init__(self, path, extractor=Extractor, recognizer=Recognizer, solver=Solver):
        """
        Initializes the Sudoku class.
        """
        self.original = cv2.imread(path)
        self.extractor = extractor
        self.recognizer = recognizer
        self.solver = solver
        

    def solve(self):
        """
        Solves the Sudoku puzzle applying some series of steps.
        """
        original_image = self.original
        e = self.extractor
        r = self.recognizer
        s = self.solver

        # Extraction: Detect the puzzle in the image and correct the perspective.
        self._save_image(original_image, 0)
        preprocessed_image = e.preprocess_image(original_image)
        self._save_image(preprocessed_image, 1)
        masked_image = e.detect_outerbox(preprocessed_image, original_image)
        self._save_image(masked_image, 2)
        intersection_image = e.detect_grid(masked_image)
        self._save_image(intersection_image, 3)
        centroids, centroids_image = e.determine_vertices(intersection_image, original_image)
        self._save_image(centroids_image, 4)
        corrected_image = e.correct_perspective(centroids, original_image)
        self._save_image(corrected_image, 5)

        # Recognition: Determine each cell and predict the digits in the cells.
        digits = r.split_digits(corrected_image)
        predicted_image, results = r.recognize_digits(digits)
        self._save_image(predicted_image, 6)

        # Solution: Solve the puzzle after checking its validity, then finally write the solution onto the original image.
        s.check_validity(results)
        solution_image = s.solve_puzzle(results)
        self._save_image(solution_image, 7)
        final_image = s.reverse_perspective(solution_image, centroids, original_image)
        self._save_image(final_image, 8)

        
    def _save_image(self, img, i):
        """
        A utility function to save the image to specified directory.
        """
        if not os.path.exists("StageImages"):
            os.makedirs("StageImages")
        try: os.remove(f"StageImages/{i}.jpg")
        except: pass
        cv2.imwrite(f"StageImages/{i}.jpg", img)