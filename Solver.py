from utils import save_image

import numpy as np
import cv2

class Solver:

    @staticmethod
    def check_validity(results):
        """
        Check the Sudoku puzzle validity.
        """
        # Check row validity
        for row in results:
            occurred = set()
            for digit in row:
                if digit == 0: continue
                elif digit in occurred: raise Exception(f'Invalid Sudoku!')
                else: occurred.add(digit) 

        # Check column validity
        for row in results.transpose():
            occurred = set()
            for digit in row:
                if digit == 0: continue
                elif digit in occurred: raise Exception(f'Invalid Sudoku!')
                else: occurred.add(digit) 

        # Check box validity
        for i in range(3):
            for j in range(3):
                box = results[3*i:3*i+3, 3*j:3*j+3].flatten()
                occurred = set()
                for digit in box:
                    if digit == 0: continue
                    elif digit in occurred: raise Exception(f'Invalid Sudoku!')
                    else: occurred.add(digit)


    @staticmethod
    def solve_puzzle(results):
        """
        Determine the remaining digits using a backtracking algorithm.
        """
        arr = results.copy()
        Solver._solve(arr)
        # Create an image of solved puzzle for display purposes
        arr[results != 0] = 0
        image_results = np.zeros((450, 450, 3), np.uint8)
        for y, row in enumerate(arr):
            for x, digit in enumerate(row):
                if digit == 0: continue
                else: cv2.putText(image_results, str(digit), (x*50+10, y*50+40), cv2.FONT_HERSHEY_DUPLEX, 1.4, (255, 0, 255), lineType=cv2.LINE_AA)
        
        # Save the images for display purposes
        save_image(image_results, 24)

        return image_results


    @staticmethod
    def _solve(arr):
        find = Solver._find_empty(arr)

        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if Solver._valid(i, (row, col), arr):
                arr[row][col] = i

                if Solver._solve(arr):
                    return True

                arr[row][col] = 0

        return False


    @staticmethod
    def _valid(num, pos, arr):
        for i in range(len(arr[0])):
            if arr[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(len(arr)):
            if arr[i][pos[1]] == num and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if arr[i][j] == num and (i,j) != pos:
                    return False
                
        return True


    @staticmethod
    def _find_empty(arr):
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if arr[i][j] == 0:
                    return (i, j)
                
        return None
    

    @staticmethod
    def reverse_perspective(img, centroids, dst):
        """
        Write the solution directly onto the original image.
        """
        blank = np.zeros((dst.shape[0], dst.shape[1], 3), np.uint8) # Create a blank image.

        for i in range(100):
            r = i // 10
            c = i % 10

            if c == 9 or r == 9: continue

            c1 = centroids[i]
            c2 = centroids[i+1]
            c3 = centroids[i+10]
            c4 = centroids[i+11]
            
            source = np.array([[50*c, 50*r], [50*c+50, 50*r], [50*c, 50*r+50], [50*c+50, 50*r+50]], dtype=np.float32) # Calculate correspording cells
            destination = np.array([c1, c2, c3, c4], dtype=np.float32) # Get the vertices of each cell in the destination image
            mat = cv2.getPerspectiveTransform(source, destination) # Get the transformation matrix
            warp = cv2.warpPerspective(img, mat, (dst.shape[1], dst.shape[0])) # Apply the transformation to the image.

            # Crop the cells roughly
            top_left_x = min([c1[1], c3[1]])
            top_left_y = min([c1[0], c3[0]])
            bot_right_x = max([c2[1], c4[1]])
            bot_right_y = max([c2[0], c4[0]])

            blank[top_left_x:bot_right_x, top_left_y:bot_right_y] = warp[top_left_x:bot_right_x, top_left_y:bot_right_y] # Build the final image one cell at a time

        # Apply mask to obtain only digits
        gray = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
        fg = cv2.bitwise_and(blank, blank, mask=mask)

        # Apply inverse of that mask to substrack the digits from the background image
        mask_inv = cv2.bitwise_not(mask)
        bg = cv2.bitwise_and(dst, dst, mask=mask_inv)

        # Add these both images together
        result = cv2.add(fg, bg)

        # Save the images for display purposes
        save_image(fg, 25)
        save_image(result, 26)

        return result