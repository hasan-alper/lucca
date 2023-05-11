import tkinter
import json
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from Sudoku import Sudoku

with open("content.json", "r") as file:
    content = json.load(file)

window = tkinter.Tk()
window.geometry("600x650")
window.title("Lucca - Sudoku Solver")

window.rowconfigure(0, minsize=120)
window.rowconfigure(1)
window.rowconfigure(2, weight=1)

window.columnconfigure(0, weight=1, minsize=480)
window.columnconfigure(1)

########## HEADER FRAME ##########
header_frame = ttk.Frame(window, relief="solid")
header_frame.grid(row=0, column=0, columnspan=2, sticky="nesw")

header_var = tkinter.StringVar(value="Home")
header_label = ttk.Label(header_frame, textvariable=header_var, font=("Helvetica", 24), relief="solid")
header_label.pack(fill="x", padx=10, pady=10)

description_var = tkinter.StringVar(value="Select an image of a Sudoku image.")
description_label = ttk.Label(header_frame, textvariable=description_var, font=("Helvetica", 16), wraplength=550, relief="solid")
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

home_button = ttk.Button(navigation_frame, text="Home", state="disabled", command=lambda: home_image())
home_button.pack(padx=10, pady=10)

back_button = ttk.Button(navigation_frame, text="Back", state="disabled", command=lambda: back_image())
back_button.pack(padx=10, pady=(0, 10))

next_button = ttk.Button(navigation_frame, text="Next", state="disabled", command=lambda: next_image())
next_button.pack(padx=10, pady=(0, 10))

skip_button = ttk.Button(navigation_frame, text="Skip", state="disabled", command=lambda: skip_image())
skip_button.pack(padx=10, pady=(0, 10))

index = 1

def upload_file():
    global index
    index = 1

    filename = filedialog.askopenfilename(filetypes=[("JPG Files", "*.jpg"), ("PNG Files", "*.png")])
    path.set(filename)

    home_button["state"] = "disabled"
    back_button["state"] = "disabled"
    next_button["state"] = "normal"
    skip_button["state"] = "normal"

    sudoku = Sudoku(filename)
    try: sudoku.solve()
    except: pass

    update_content(index)

def home_image():
    global index
    index = 1

    update_content(index)

    home_button["state"] = "disabled"
    back_button["state"] = "disabled"
    next_button["state"] = "normal"
    skip_button["state"] = "normal"


def back_image():
    global index
    index -= 1

    update_content(index)

    try:
        Image.open(f"StageImages/{index-1}.jpg")
    except FileNotFoundError:
        home_button["state"] = "disabled"
        back_button["state"] = "disabled"
    else:
        back_button["state"] = "normal"
    finally:
        next_button["state"] = "normal"
        skip_button["state"] = "normal"


def next_image():
    global index
    index += 1

    update_content(index)

    try:
        Image.open(f"StageImages/{index+1}.jpg")
    except FileNotFoundError:
        next_button["state"] = "disabled"
        skip_button["state"] = "disabled"
    else:
        next_button["state"] = "normal"
    finally:
        back_button["state"] = "normal"
        home_button["state"] = "normal"


def skip_image():
    global index
    
    for i in range(30):
        try:
            Image.open(f"StageImages/{index+1}.jpg")
            index = i
        except FileNotFoundError:
            break

    update_content(index)

    home_button["state"] = "normal"
    back_button["state"] = "normal"
    next_button["state"] = "disabled"
    skip_button["state"] = "disabled"

def update_content(i):
    image = Image.open(f"StageImages/{i}.jpg")
    image.thumbnail((450, 450))
    tk_image = ImageTk.PhotoImage(image)
    image_label["image"] = tk_image
    image_label.image = tk_image

    header_var.set(content[i-1]["header"])
    description_var.set(content[i-1]["description"])


window.mainloop()