import numpy as np
import cv2
import os

class Solver:
    def __init__(self, arr):
        self.arr = arr
        self.results = arr.copy()

    def check_validity(self):
        # Check row validity
        for row in self.arr:
            occurred = set()
            for digit in row:
                if digit == 0: continue
                elif digit in occurred: raise Exception(f'Invalid Sudoku!')
                else: occurred.add(digit) 

        # Check column validity
        for row in self.arr.transpose():
            occurred = set()
            for digit in row:
                if digit == 0: continue
                elif digit in occurred: raise Exception(f'Invalid Sudoku!')
                else: occurred.add(digit) 

        # Check box validity
        for i in range(3):
            for j in range(3):
                box = self.arr[3*i:3*i+3, 3*j:3*j+3].flatten()
                occurred = set()
                for digit in box:
                    if digit == 0: continue
                    elif digit in occurred: raise Exception(f'Invalid Sudoku!')
                    else: occurred.add(digit)

    def solve_puzzle(self):
        self._solve()
        # Create an image of solved puzzle for display purposes
        self.results[self.arr != 0] = 0
        image_results = np.zeros((450, 450, 3), np.uint8)
        for y, row in enumerate(self.results):
            for x, digit in enumerate(row):
                if digit == 0: continue
                else: cv2.putText(image_results, str(digit), (x*50+10, y*50+40), cv2.FONT_HERSHEY_DUPLEX, 1.4, (255, 0, 255), lineType=cv2.LINE_AA)
        
        self._write_images(image_results, 10)
        self.image = image_results

    def _solve(self):
        find = self._find_empty()

        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self._valid(i, (row, col)):
                self.results[row][col] = i

                if self._solve():
                    return True

                self.results[row][col] = 0
        return False


    def _valid(self, num, pos):
        for i in range(len(self.results[0])):
            if self.results[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(self.results)):
            if self.results[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.results[i][j] == num and (i,j) != pos:
                    return False
        return True

    def _find_empty(self):
        for i in range(len(self.results)):
            for j in range(len(self.results[0])):
                if self.results[i][j] == 0:
                    return (i, j)
        return None
    
    def _write_images(self, img, i):
        try: os.remove(f"StageImages/{i}.jpg")
        except: pass
        cv2.imwrite(f"StageImages/{i}.jpg", img)