import os, shutil, cv2

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

        # Reset the stage images before running the code.
        try:
            shutil.rmtree("StageImages")
        except: pass
        os.makedirs("StageImages")

        # Extraction: Detect the puzzle in the image and correct the perspective.
        preprocessed_image = e.preprocess_image(original_image)
        masked_image = e.detect_outerbox(preprocessed_image, original_image)
        intersection_image = e.detect_grid(masked_image)
        centroids = e.determine_vertices(intersection_image, original_image)
        corrected_image = e.correct_perspective(centroids, original_image)

        # Recognition: Determine each cell and predict the digits in the cells.
        digits = r.split_digits(corrected_image)
        results = r.recognize_digits(digits)

        # Solution: Solve the puzzle after checking its validity, then finally write the solution onto the original image.
        s.check_validity(results)
        solution_image = s.solve_puzzle(results)
        final_image = s.reverse_perspective(solution_image, centroids, original_image)
