import tkinter
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

window = tkinter.Tk()
window.geometry("600x650")
window.title("Lucca - Sudoku Solver")

window.rowconfigure(0, weight=1, minsize=90)
window.rowconfigure(1)
window.rowconfigure(2, weight=1)

window.columnconfigure(0, weight=1, minsize=480)
window.columnconfigure(1)

########## HEADER FRAME ##########
header_frame = ttk.Frame(window, relief="solid")
header_frame.grid(row=0, column=0, columnspan=2, sticky="nesw")

header_label = ttk.Label(header_frame, text="Preview", font=("Helvetica", 24), relief="solid")
header_label.pack(fill="x", padx=10, pady=10)

description_label = ttk.Label(header_frame, text="Select an image of a Sudoku image.", font=("Helvetica", 16), relief="solid")
description_label.pack(fill="x", padx=10, pady=(0, 10))


########### PATH FRAME ###########
path_frame = ttk.Frame(window, relief="solid")
path_frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

upload_button = ttk.Button(path_frame, text="Open", command=lambda: upload_file())
upload_button.pack(side="left", padx=10, pady=10)

path = tkinter.StringVar(value="No Image Selected")
upload_label = ttk.Label(path_frame, textvariable=path, font=("Helvetica", 16), relief="solid")
upload_label.pack(expand=True, fill="x", padx=10, pady=10)


########## RESULT FRAME ##########
result_frame = ttk.Frame(window, relief="solid")
result_frame.grid(row=2, column=0, sticky="nesw")

image = Image.open("Screenshots/no-image.jpg")
image.thumbnail((450, 450))
tk_image = ImageTk.PhotoImage(image)
image_label = ttk.Label(result_frame, image=tk_image, relief="solid")
image_label.pack(padx=10, pady=10)


######## NAVIGATION FRAME ########
navigation_frame = ttk.Frame(window, relief="solid")
navigation_frame.grid(row=2, column=1, sticky="nesw")

back_button = ttk.Button(navigation_frame, text="Back")
back_button.pack(padx=10, pady=10)

next_button = ttk.Button(navigation_frame, text="Next")
next_button.pack(padx=10, pady=(0, 10))


def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("JPG Files", "*.jpg"), ("PNG Files", "*.png")])
    path.set(filename)
    image = Image.open(filename)
    image.thumbnail((450, 450))
    tk_image = ImageTk.PhotoImage(image)
    image_label["image"] = tk_image
    image_label.image = tk_image


window.mainloop()


# from Sudoku import Sudoku

# sudoku = Sudoku("TestImages/sudoku-1.jpg")
# sudoku.solve()