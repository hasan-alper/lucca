
class Solver:
    def __init__(self, arr):
        self.arr = arr

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