import tkinter
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

window = tkinter.Tk()
window.geometry("1000x600")
window.title("Lucca - Sudoku Solver")

header_label = ttk.Label(window, text="Preview", font=("Helvetica", 24))
header_label.pack()

description_label = ttk.Label(window, text="Select an image of a Sudoku image.", font=("Helvetica", 16))
description_label.pack()

upload_button = ttk.Button(window, text="Open", command=lambda: upload_file())
upload_button.pack()

path = tkinter.StringVar(value="No Image Selected")
upload_label = ttk.Label(window, textvariable=path, font=("Helvetica", 16))
upload_label.pack()

image_label = ttk.Label(window)
image_label.pack()

def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("JPG Files", "*.jpg"), ("PNG Files", "*.png")])
    path.set(filename)
    image = Image.open(filename).resize((450, 450))
    tk_image = ImageTk.PhotoImage(image)
    image_label["image"] = tk_image
    image_label.image = tk_image


window.mainloop()


# from Sudoku import Sudoku

# sudoku = Sudoku("TestImages/sudoku-1.jpg")
# sudoku.solve()