import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import importlib
import logging
from datetime import datetime
import subprocess
logging.basicConfig(filename='installation.log', level=logging.ERROR, format='%(asctime)s %(message)s')

version = 2.1
modules = ["PyQt5", "tkinter", "pillow", "flask", "threading", "socket"]

def check_module(module_name, progressbar):
    try:
        importlib.import_module(module_name)
        print(f"{module_name} is already installed.")
    except ImportError:
        try:
            result = subprocess.run(f"pip install {module_name}", shell=True, capture_output=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Encounterd error during installation of {module_name}\n{result.stderr.decode()}")
                raise Exception(result.stderr.decode())
            print(f"{module_name} has been installed.")
        except Exception as e:
            logging.error(f"Encounterd error during installation of {module_name}: {e}")
            messagebox.showerror("Error", f"Encounterd error during installation of {module_name}\n{e}")
    progressbar.step()
    root.update_idletasks()

def update_gui():
    try:
        # Delete old GUI files stored in the Documents
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents')
        py_dir = os.path.join(user_doc, 'py')
        os.remove(os.path.join(py_dir, 'player.py'))
        
        # Delete old GUI file stored on the desktop
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        os.remove(os.path.join(desktop_path, 'gui_2.1.py'))
        
        # Copy new GUI files to the Documents
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, 'files')
        shutil.copy(os.path.join(files_dir, 'player.py'), py_dir)
        
        # Copy new GUI file to the desktop
        shutil.copy(os.path.join(files_dir, 'gui_2.1.py'), desktop_path)
        messagebox.showinfo("Update", "Player GUI has been updated.")
        root.destroy()
        os._exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"Encounterd error during updating of GUI \n{e}")

def download():
    try:
        progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", maximum=len(modules))
        progressbar.pack()
        progressbar.start()
        for module in modules:
            check_module(module, progressbar)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, 'files')
        files = os.listdir(files_dir)
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents')
        py_dir = os.path.join(user_doc, 'py')
        os.makedirs(py_dir, exist_ok=True)

        for file in files:
            file_path = os.path.join(files_dir, file)
            dest_path = os.path.join(py_dir, file)
            if os.path.isfile(dest_path):
                print(f"{file} already exists in {py_dir}, skipping.")
                continue
            try:
                shutil.copy(file_path, py_dir)
                print(f"{file} has been copied to {py_dir}")
            except error as error:
                messagebox.showerror("Error", f"Encounterd error during installation of \n{e}")
                logging.error(f"Encounterd error during copying of the files: {error}")
        if place_on_desktop_var.get() == 0:
            progressbar.stop()
            messagebox.showinfo("Download", "Installation done")
            root.destroy()
            os._exit(0)
        place_on_desktop(progressbar)
    except Exception as e:
         logging.error(f"Encounterd error during installation of: {e}")
         messagebox.showerror("Error", f"Encounterd error during installation of \n{e}")

def place_on_desktop(progressbar):
    try:
        if place_on_desktop_var.get() == 1:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            files_dir = os.path.join(current_dir, 'files')
            if not os.path.exists(files_dir):
                raise FileNotFoundError("files_dir does not exist.")
            gui_file_path = os.path.join(files_dir, f'gui_{version}.py')
            desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            desktop_file_path = os.path.join(desktop_dir, 'gui.py')
            if os.path.isfile(desktop_file_path):
                print(f"{gui_file_path} already exists on desktop, skipping.")
            shutil.copy(gui_file_path, desktop_dir)
            print(f"{gui_file_path} has been copied to {desktop_dir}")
            progressbar.stop()
            messagebox.showinfo("Download", "Installation done")
            root.destroy()
            os._exit(0)
    except error as error:
        logging.error(f"Encounterd error during placing on desktop: {error}")
        progressbar.stop()
        messagebox.showerror("Error", f"Encounterd error during Placing on desktop \n{error}")



if not sys.version:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Python is not installed or version not detected")
    quit()
else:
    print(sys.version)

root = tk.Tk()
root.title("File Downloader")
root.geometry("600x600")
place_on_desktop_var = tk.IntVar()
place_on_desktop_checkbox = tk.Checkbutton(root, text="Place GUI on desktop", variable=place_on_desktop_var, font=("", 20), width=30, height=2)
place_on_desktop_checkbox.pack()
download_button = tk.Button(root, width=15,height=5, text="Download", command=download)
download_button.pack()
update_button = tk.Button(root, text="Update", command=update_gui)
update_button.pack()
root.mainloop()