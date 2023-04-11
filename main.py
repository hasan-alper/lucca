from Extractor import Extractor
from Recognizer import Recognizer

extractor = Extractor("TestImages/sudoku-1.png")

extractor.preprocess_image()
extractor.detect_grid()
extractor.detect_lines()
extractor.detect_vertices()
extractor.correct_perspective()

recognizer = Recognizer(extractor.image)

recognizer.split_digits()
recognizer.recognize_digits()

