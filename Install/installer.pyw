import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import importlib

version = 2.1
modules = ["PyQt5", "tkinter", "pillow", "flask", "threading", "socket"]

def check_module(module_name, progressbar):
    try:
        importlib.import_module(module_name)
        print(f"{module_name} is already installed.")
    except ImportError:
        os.system(f"pip install {module_name}")
        print(f"{module_name} has been installed.")
    progressbar.step()
    root.update()

def download():
    progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", maximum=len(modules))
    progressbar.pack()
    progressbar.start()
    for module in modules:
        check_module(module, progressbar)
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
    if place_on_desktop_var.get() == 0:
        progressbar.stop()
        root.destroy()
        os._exit(0)
    place_on_desktop()

def place_on_desktop():
    if place_on_desktop_var.get() == 1:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, 'files')
        gui_file_path = os.path.join(files_dir, f'gui_{version}.py')
        desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        desktop_file_path = os.path.join(desktop_dir, 'gui.py')
        if os.path.isfile(desktop_file_path):
            print(f"{gui_file_path} already exists on desktop, skipping.")
        shutil.copy(gui_file_path, desktop_dir)
        print(f"{gui_file_path} has been copied to {desktop_dir}")
        root.destroy()
        os._exit(0)



if not sys.version:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Python is not installed or version not detected")
    quit()
else:
    print(sys.version)

root = tk.Tk()
root.title("File Downloader")
place_on_desktop_var = tk.IntVar()
place_on_desktop_checkbox = tk.Checkbutton(root, text="Place GUI on desktop", variable=place_on_desktop_var)
place_on_desktop_checkbox.pack()
download_button = ttk.Button(root, text="Download", command=download)
download_button.pack()

root.mainloop()