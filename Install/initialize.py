import os
import shutil
import tkinter as tk
from tkinter import ttk

version = 2.1

def download():
    # Your existing download function here
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(current_dir, 'files')
    files = os.listdir(files_dir)
    user_doc = os.path.join(os.environ['USERPROFILE'], 'Documents')
    py_dir = os.path.join(user_doc, 'py')
    os.makedirs(py_dir, exist_ok=True)

    for file in files:
        file_path = os.path.join(files_dir, file)
        dest_path = os.path.join(py_dir, file)
        if os.path.isfile(dest_path):
            print(f"{file} already exists in {py_dir}, skipping.")
            continue
        shutil.copy(file_path, py_dir)
        print(f"{file} has been copied to {py_dir}")
    place_on_desktop()

def place_on_desktop():
    print("yes")
    if place_on_desktop_var.get() == 1:
        print("yesyes")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, 'files')
        # Get the path to the "gui.py" file
        gui_file_path = os.path.join(files_dir, f'gui_{version}.py')
        # Get the current user's desktop directory
        desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        # Construct the full path to the destination on the desktop
        desktop_file_path = os.path.join(desktop_dir, 'gui.py')
        # Check if the file already exists on the desktop
        if os.path.isfile(desktop_file_path):
            print(f"{gui_file_path} already exists on desktop, skipping.")
        # Otherwise, copy the file to the desktop
        shutil.copy(gui_file_path, desktop_dir)
        print(f"{gui_file_path} has been copied to {desktop_dir}")

        
root = tk.Tk()
root.title("File Downloader")

place_on_desktop_var = tk.IntVar()
place_on_desktop_checkbox = tk.Checkbutton(root, text="Place GUI on desktop", variable=place_on_desktop_var)
place_on_desktop_checkbox.pack()

download_button = ttk.Button(root, text="Download", command=download)
download_button.pack()

root.mainloop()