# Lucca - A Sudoku Solver
A sudoku solver that tries to extract the puzzle from a photo and solve it.

## About
This application allows users to quickly and easily solve a Sudoku puzzle by simply taking a picture of the puzzle with their camera. The image is then processed using some image processing techniques to extract the puzzle from the background and identify each individual cell. Next, a convolutional neural network (CNN) model, trained on the MNSIT dataset, is used to accurately predict the digits in each cell. Once all the digits have been identified, a backtracking algorithm is employed to solve the puzzle. Finally, the solution is written directly onto the original image.

## Stages
Here are some of the steps of this process:

### Import The Image

Import a sudoku puzzle image.

![](Screenshots/0.jpg)

### Process The Image

Convert the image to grayscale and apply some blur to reduce the noise.

![](Screenshots/1.jpg)

### Find The Outerbox

Apply thresholding and find the biggest contour. Then get rid of the parts outside the box.

![](Screenshots/2.jpg)

### Determine The Vertices

Determine the intersections of the lines.

![](Screenshots/3.jpg)

### Find The Coordinates of the Vertices

Find the coordinates of the vertices to used them later in the transformation step.

![](Screenshots/4.jpg)

### Transform The Image

Correct the perspective to find the digits easily later in the process

![](Screenshots/5.jpg)

### Identify The Digits

Predict the digits in the puzzle.

![](Screenshots/6.jpg)

### Solve The Puzzle

Determine the remaining digits using a backtracking algorithm.

![](Screenshots/7.jpg)

### Finalize The Solution

Write the solution directly onto the original image.

![](Screenshots/8.jpg)

## Installation
In order to play around with the project, you can set up this repository locally following these simple steps.

Note that in order to avoid potential conflicts with other packages, it is strongly recommended to use a virtual environment or a conda environment.

1. Clone the repo
    ```sh
    git clone https://github.com/hasan-alper/lucca.git
    ```
2. Move inside your copy
    ```sh
    cd lucca
    ```
3. Create a virtual environment
    ```sh
    virtualenv [my_virtual_env_name]
    ```
4. Active the virtual environment
    ```sh
    source [my_virtual_env_name]/bin/activate
    ```
5. Install necessary packages
    ```sh
    pip install -r requirements.txt
    ```

## Contributing

Any contributions are welcome. Feel free to create a pull request to improve one or two things. If you find any bugs/issues, you can also simply open an issue.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.