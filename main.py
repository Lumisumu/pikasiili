import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import colorchooser
import os
import glob
import subprocess
import threading
from PIL import Image, ImageTk

# Set working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def choose_color():
    # Open color picker
    code_color = str(colorchooser.askcolor()[0])

    # Color into hex
    rgb_values = code_color.strip("()").split(", ")
    r, g, b = map(int, rgb_values)
    color_hex = ('{:02X}' * 3).format(r, g, b)
    color_hex = "#" + color_hex
    print("User picked color: " + str(code_color) + " / " + color_hex)

    # Insert into field
    color_field.delete(0, tk.END)
    color_field.insert(0, str(color_hex))

# User chooses folder
def choose_folder():
    selected_folder = askdirectory()

    # Replace field text
    object_folder_field.delete(0, tk.END)
    object_folder_field.insert(0, selected_folder)

# Run command when Run button is pressed
def run_command(current_command: str, folder: str):
    thread = threading.Thread(target=start_thread(current_command, folder))
    thread.start()

def start_thread(command: str, folder: str):
    subprocess.Popen(["cmd", "/c", f"start cmd /c {command}"], cwd=folder, shell=True)

# Open text file for editing
def open_file(name):
    file_path = "userdata\\" + name + ".txt"

    if os.path.exists(file_path):
        print(f"{file_path} is opened for editing.")
        os.startfile(file_path)
    else:
        print(f"{file_path} cannot be opened, it was not found.")

# Remove text file
def remove_project(name):
    file_path = "userdata\\" + name + ".txt"

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} was removed.")
    else:
        print(f"{file_path} cannot be removed, it was not found.")

    update_objects_list()

# Open project folder
def show_folder(folder):
    if os.path.exists(folder):
        os.startfile(folder)
    else:
        print("Path invalid, cannot find directory.")

# Update objects list
def update_objects_list():
    # Variables
    all_objects = []

    # Clear rows which show projects
    for widget in canvas_inner.winfo_children():
        widget.destroy()

    # Go through all text files
    for file_name in glob.glob(os.path.join("userdata", "*.txt")):
        # Read the file and save lines to variables
        with open(file_name, "r", encoding="utf-8") as file:
            object_name = file.readline().strip()
            folder_name = file.readline().strip()
            command_text = file.readline().strip()
            bg_color = file.readline().strip()

            # Get number of rows
            current_row = len(all_objects)

            # Grid for project info and buttons
            object_frame = tk.Frame(canvas_inner, bg=bg_color)
            object_frame.grid(row=current_row, column=0, sticky="news")
            object_frame.columnconfigure(0, weight=1)
            object_frame.columnconfigure(1, weight=1)
            object_frame.columnconfigure(2, weight=1)
            object_frame.columnconfigure(3, weight=1)
            object_frame.columnconfigure(4, weight=1)
            object_frame.rowconfigure(0, weight=1)

            all_objects.append(object_frame)

            # Object name
            object_name_label = tk.Label(object_frame, text=object_name, font=('Arial', 12), height=1, width=15, anchor="w")
            object_name_label.grid(row=0, column=0, sticky="nws", padx=5, pady=5)

            # Edit button
            edit_button = tk.Button(object_frame, text="Edit", font=('Arial', 12), command=lambda line=object_name: open_file(line), bg="#b0b0b0", width=8)
            edit_button.grid(row=0, column=1, sticky="news", padx=5, pady=5)

            # Remove button
            remove_button = tk.Button(object_frame, text="Remove", font=('Arial', 12), command=lambda line=object_name: remove_project(line), bg="#d59098", width=8)
            remove_button.grid(row=0, column=2, sticky="news", padx=5, pady=5)

            # Show folder button
            show_button = tk.Button(object_frame, text="Show files", font=('Arial', 12), command=lambda folder=folder_name: show_folder(folder), bg="#90c4d5", width=10)
            show_button.grid(row=0, column=3, sticky="news", padx=5, pady=5)

            # Run button
            run_button_text = "Run " + object_name
            run_button = tk.Button(object_frame, text=run_button_text, font=('Arial', 13), command=lambda line=command_text, folder=folder_name,: run_command(line, folder), bg="#9de2a1", width=20)
            run_button.grid(row=0, column=4, sticky="news", padx=5, pady=5)

    update_scrolling()

# Add new object
def add_new_object():
    # Gather text from input fields
    new_object_name = object_name_field.get().rstrip().lstrip()

    if new_object_name == "":
        print("Name field was empty, project cannot be created.")
        return

    new_folder_name = object_folder_field.get().rstrip().lstrip()
    new_command_text = object_commands_field.get().rstrip().lstrip()
    new_color = color_field.get().rstrip().lstrip()

    if new_color == "":
        print("Color was empty, using default white")
        new_color = "white"

    target_file = "userdata/" + new_object_name + ".txt"

    # Create a text file to save input
    if not os.path.exists("userdata"):
        os.makedirs("userdata")

    with open(target_file, "w") as file:
        file.write(new_object_name + "\n")
        file.write(new_folder_name + "\n")
        file.write(new_command_text + "\n")
        file.write(new_color + "\n")

    # Update the objects list
    update_objects_list()

    # Clear input fields
    object_name_field.delete(0, tk.END)
    object_folder_field.delete(0, tk.END)
    object_commands_field.delete(0, tk.END)
    color_field.delete(0, tk.END)

def update_scrolling():
    canvas.configure(scrollregion=canvas.bbox("all"))

def resize_canvas(event):
    canvas.itemconfig(canvas_window, width=event.width)

# Main application window
root = tk.Tk()
root.title("Pikasiili")
root.geometry("670x600")
root.iconbitmap("res/pikasiili-icon.ico")
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=6)
root.columnconfigure(0, weight=1)

# Image
image = Image.open("res/pikasiili-icon.ico")
image = image.resize((80, 80), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
root.photo = photo

# Frame, resizing canvas and scrollbar for scrolling area
scrolling_frame = tk.Frame(root)
scrolling_frame.grid(row=1, column=0, sticky="news")
scrolling_frame.rowconfigure(0, weight=1)
scrolling_frame.columnconfigure(0, weight=1)
canvas = tk.Canvas(scrolling_frame, bg="white")
canvas.grid(row=0, column=0, sticky="news")
scrollbar = tk.Scrollbar(scrolling_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.configure(yscrollcommand=scrollbar.set)
canvas_inner = tk.Frame(canvas)
canvas_inner.bind("<Configure>", lambda event: update_scrolling())
canvas_window = canvas.create_window((0, 0), window=canvas_inner, anchor="nw")
canvas.bind("<Configure>", resize_canvas)

# Grids for input fields and button
controls_frame = tk.Frame(root)
controls_frame.grid(row=0, column=0, sticky="news")
controls_frame.columnconfigure(0, weight=1)
controls_frame.columnconfigure(1, weight=1)
controls_frame.rowconfigure(0, weight=1)

# Grid for fields for new object details
fields_frame = tk.Frame(controls_frame)
fields_frame.grid(row=0, column=0, sticky="news")
fields_frame.columnconfigure(0, weight=1)
fields_frame.columnconfigure(1, weight=3)
fields_frame.columnconfigure(2, weight=1)
fields_frame.rowconfigure(0, weight=1)
fields_frame.rowconfigure(1, weight=1)
fields_frame.rowconfigure(2, weight=1)
fields_frame.rowconfigure(3, weight=1)

# Fields for input
object_name_label = tk.Label(fields_frame, text="Name*", font=('Arial', 13), height = 1, width=5).grid(row=0, column=0, sticky="e")
object_name_field = tk.Entry(fields_frame, justify="left", font=('Arial', 13))
object_name_field.grid(row=0, column=1, padx=15, sticky="ew")

object_folder_label = tk.Label(fields_frame, text="Folder*", font=('Arial', 13), height = 1).grid(row=1, column=0, sticky="e")
object_folder_field = tk.Entry(fields_frame, justify="left", font=('Arial', 13))
object_folder_field.grid(row=1, column=1, padx=15, sticky="ew")
choose_folder_button = tk.Button(fields_frame, text="Choose folder", font=('Arial', 12), command=choose_folder, height = 1, width = 12).grid(row=1, column=2, sticky="nws", padx=5, pady=5)

object_commands_label = tk.Label(fields_frame, text="Command*", font=('Arial', 13), height = 1).grid(row=2, column=0, sticky="e")
object_commands_field = tk.Entry(fields_frame, justify="left", font=('Arial', 13))
object_commands_field.grid(row=2, column=1, padx=15, sticky="ew")

color_label = tk.Label(fields_frame, text="Background color", font=('Arial', 13), height = 1).grid(row=3, column=0, sticky="e")
color_field = tk.Entry(fields_frame, justify="left", font=('Arial', 13))
color_field.grid(row=3, column=1, padx=15, sticky="ew")
color_button = tk.Button(fields_frame, text="Change", font=('Arial', 12), command=choose_color, height = 1, width = 12).grid(row=3, column=2, sticky="nws", padx=5, pady=5)

# Button that adds objects
add_button = tk.Button(controls_frame, text="Add project", font=('Arial', 13), image=photo, compound="top", height = 1, width=20, command=lambda: add_new_object())
add_button.grid(row=0, column=1, pady=5, padx=5, sticky="news")

update_objects_list()

root.mainloop()