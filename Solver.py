
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

                    

    def solve(self):
        find = self._find_empty()

        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self._valid(i, (row, col)):
                self.arr[row][col] = i

                if self.solve():
                    return True

                self.arr[row][col] = 0
        return False


    def _valid(self, num, pos):
        for i in range(len(self.arr[0])):
            if self.arr[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(self.arr)):
            if self.arr[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.arr[i][j] == num and (i,j) != pos:
                    return False
        return True

    def _find_empty(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[0])):
                if self.arr[i][j] == 0:
                    return (i, j)
        return None