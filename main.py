import tkinter, cv2, json, os
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from Sudoku import Sudoku

with open("content.json", "r") as file:
    content = json.load(file)

window = tkinter.Tk()
window.geometry("640x720")
window.title("Lucca - Sudoku Solver")

window.rowconfigure(0, minsize=115)
window.rowconfigure(1, weight=1, minsize=5) # Separator
window.rowconfigure(2)
window.rowconfigure(3, weight=1, minsize=5) # Separator
window.rowconfigure(4, weight=1, minsize=480)

window.columnconfigure(0, weight=1, minsize=480)
window.columnconfigure(1, weight=1, minsize=5) # Separator
window.columnconfigure(2)

window.bind("<q>", lambda e: window.destroy())
window.bind("<o>", lambda e: upload_file())
window.bind("<c>", lambda e: open_camera())

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 17), foreground="#444")
style.configure("TButton", width=7, padding=5)
style.configure("nav.TButton", width=5)


########## HEADER FRAME ##########
header_frame = ttk.Frame(window)
header_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=(15, 10), sticky="nesw")

header_var = tkinter.StringVar(value="Home")
header_label = ttk.Label(header_frame, textvariable=header_var, font=("Helvetica", 28), foreground="#000")
header_label.pack(fill="x")

description_var = tkinter.StringVar(value="Start by uploading an image of a Sudoku.")
description_label = ttk.Label(header_frame, textvariable=description_var, wraplength=600)
description_label.pack(fill="x", pady=(10, 0))


##### HEADER SEPARATOR FRAME #####
header_separator_frame = ttk.Frame(window)
header_separator_frame.grid(row=1, column=0, columnspan=3, padx=10, sticky="nesw")

header_separator = ttk.Separator(header_separator_frame, orient='horizontal')
header_separator.pack(side="bottom", fill="x")


########### PATH FRAME ###########
path_frame = ttk.Frame(window)
path_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nesw")

upload_button = ttk.Button(path_frame, text="Open...", command=lambda: upload_file())
upload_button.grid(row=0, column=0)

camera_button = ttk.Button(path_frame, text="Camera...", command=lambda: open_camera())
camera_button.grid(row=1, column=0)

path = tkinter.StringVar(value="No Image Selected")
upload_label = ttk.Label(path_frame, textvariable=path, font=("Helvetica", 15))
upload_label.grid(row=0, column=1, rowspan=2, padx=15, sticky="nesw")


###### PATH SEPARATOR FRAME ####3#
path_separator_frame = ttk.Frame(window)
path_separator_frame.grid(row=3, column=0, columnspan=3, padx=10, sticky="nesw")

path_separator = ttk.Separator(path_separator_frame, orient='horizontal')
path_separator.pack(fill="x")


########## RESULT FRAME ##########
result_frame = ttk.Frame(window)
result_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nesw")

image = Image.open("media/no-image.jpg")
image.thumbnail((450, 450))
tk_image = ImageTk.PhotoImage(image)
image_label = ttk.Label(result_frame, image=tk_image)
image_label.pack(padx=10, pady=10)


### NAVIGATION SEPARATOR FRAME ###
navigation_separator_frame = ttk.Frame(window)
navigation_separator_frame.grid(row=4, column=1, pady=10, sticky="nesw")

navigation_separator = ttk.Separator(navigation_separator_frame, orient='vertical')
navigation_separator.pack(side="left", fill="y")


######## NAVIGATION FRAME ########
navigation_frame = ttk.Frame(window)
navigation_frame.grid(row=4, column=2, padx=10, pady=10, sticky="nesw")

home_button = ttk.Button(navigation_frame, text="Home", state="disabled", style="nav.TButton", command=lambda: home_image())
home_button.pack()

back_button = ttk.Button(navigation_frame, text="Back", state="disabled", style="nav.TButton", command=lambda: back_image())
back_button.pack()

next_button = ttk.Button(navigation_frame, text="Next", state="disabled", style="nav.TButton", command=lambda: next_image())
next_button.pack()

skip_button = ttk.Button(navigation_frame, text="Skip", state="disabled", style="nav.TButton", command=lambda: skip_image())
skip_button.pack()

save_separator = ttk.Separator(navigation_frame, orient='horizontal')
save_separator.pack(side="top", fill="x", pady=10)

save_button = ttk.Button(navigation_frame, text="Save...", state="disabled", style="nav.TButton", command=lambda: save_image())
save_button.pack()

shortcut_button = ttk.Button(navigation_frame, text="Shortcuts...", width=8, command=lambda: open_shortcuts())
shortcut_button.pack(side="bottom")


index = 1

def upload_file():
    global index
    index = 1

    filename = filedialog.askopenfilename(title="Select a Sudoku image.", filetypes=[("JPG Files", "*.jpg"), ("PNG Files", "*.png")])
    if not filename: return
    path.set(filename)

    disable_home(True)
    disable_back(True)
    disable_next(False)
    disable_skip(False)
    disable_save(False)

    sudoku = Sudoku(filename)
    try: sudoku.solve()
    except: pass

    update_content(index)


def open_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera. Press 'c' to capture, 'q' to quit.", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return
        elif key == ord('c'):
            height = frame.shape[0]
            width = frame.shape[1]
            x = min(height, width)
            frame = frame[(height-x)//2:(height-x)//2 + x, (width-x)//2:(width-x)//2 + x]
            cv2.imwrite("capture.png", frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    global index
    index = 1

    filename = "capture.png"
    path.set(os.path.abspath(filename))

    disable_home(True)
    disable_back(True)
    disable_next(False)
    disable_skip(False)
    disable_save(False)

    sudoku = Sudoku(filename)
    try: sudoku.solve()
    except: pass
    update_content(index)


def home_image():
    global index
    index = 1

    update_content(index)

    disable_home(True)
    disable_back(True)
    disable_next(False)
    disable_skip(False)


def back_image():
    global index
    index -= 1

    update_content(index)

    try:
        Image.open(f"StageImages/{index-1}.jpg")
    except FileNotFoundError:
        disable_home(True)
        disable_back(True)
    else:
        disable_back(False)
    finally:
        disable_next(False)
        disable_skip(False)


def next_image():
    global index
    index += 1

    update_content(index)

    try:
        Image.open(f"StageImages/{index+1}.jpg")
    except FileNotFoundError:
        disable_next(True)
        disable_skip(True)
    else:
        disable_next(False)
    finally:
        disable_back(False)
        disable_home(False)


def skip_image():
    global index
    
    for i in range(30):
        try:
            Image.open(f"StageImages/{index+1}.jpg")
            index = i
        except FileNotFoundError:
            break

    update_content(index)

    disable_home(False)
    disable_back(False)
    disable_next(True)
    disable_skip(True)

def save_image():
    global index

    result = filedialog.asksaveasfilename(title="Select a folder.", filetypes=[("JPG Files", "*.jpg"), ("PNG Files", "*.png")])
    print(result)
    image = Image.open(f"StageImages/{index}.jpg")
    image.save(result)
    

def open_shortcuts():
    menu = tkinter.Toplevel(window)
    menu.geometry("400x270")
    menu.title("Keyboard Shortcuts")
    menu.bind("<q>", lambda e: menu.destroy())

    ttk.Label(menu, text="<q> Quit the app.").pack(pady=(20, 2))
    ttk.Label(menu, text="<c> Open the camera.").pack(pady=2)
    ttk.Label(menu, text="<o> Open the file explorer.").pack(pady=2)
    ttk.Label(menu, text="<Up> Go to the original image.").pack(pady=2)
    ttk.Label(menu, text="<Down> Go to the result image.").pack(pady=2)
    ttk.Label(menu, text="<Left> Go to the previous image.").pack(pady=2)
    ttk.Label(menu, text="<Right> Go to the next image.").pack(pady=2)
    ttk.Label(menu, text="<s> Save the current image.").pack(pady=2)

    menu.mainloop()  


def update_content(i):
    image = Image.open(f"StageImages/{i}.jpg")
    image.thumbnail((450, 450))
    tk_image = ImageTk.PhotoImage(image)
    image_label["image"] = tk_image
    image_label.image = tk_image

    header_var.set(content[i-1]["header"])
    description_var.set(content[i-1]["description"])


def disable_home(state):
    if state:
        home_button["state"] = "disabled"
        window.unbind("<Up>")
    else:
        home_button["state"] = "normal"
        window.bind("<Up>", lambda e: home_image())


def disable_back(state):
    if state:
        back_button["state"] = "disabled"
        window.unbind("<Left>")
    else:
        back_button["state"] = "normal"
        window.bind("<Left>", lambda e: back_image())

        
def disable_next(state):
    if state:
        next_button["state"] = "disabled"
        window.unbind("<Right>")
    else:
        next_button["state"] = "normal"
        window.bind("<Right>", lambda e: next_image())


def disable_skip(state):
    if state:
        skip_button["state"] = "disabled"
        window.unbind("<Down>")
    else:
        skip_button["state"] = "normal"
        window.bind("<Down>", lambda e: skip_image())


def disable_save(state):
    if state:
        save_button["state"] = "disabled"
        window.unbind("s")
    else:
        save_button["state"] = "normal"
        window.bind("s", lambda e: save_image())


window.mainloop()