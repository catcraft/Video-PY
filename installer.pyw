import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import importlib
import logging
from datetime import datetime
import subprocess
import requests

logging.basicConfig(filename='installation.log', level=logging.ERROR, format='%(asctime)s %(message)s')

def installgui(path):
        url = 'https://raw.githubusercontent.com/catcraft/Video-Player/main/Install/files/gui.py'
        r = requests.get(url, allow_redirects=True)
        file_name = os.path.basename(url)
        open(path + "\\" + file_name, 'wb').write(r.content)

def installplayer(path):
        url = 'https://raw.githubusercontent.com/catcraft/Video-Player/main/Install/files/player.py'
        r = requests.get(url, allow_redirects=True)
        file_name = os.path.basename(url)
        open(path + "\\" + file_name, 'wb').write(r.content)
        

def installbg(path):
        url = 'https://raw.githubusercontent.com/catcraft/Video-Player/main/Install/files/bg.png'
        r = requests.get(url, allow_redirects=True)
        file_name = os.path.basename(url)
        open(path + "\\" + file_name, 'wb').write(r.content)

def installconfig(path):
        url = 'https://raw.githubusercontent.com/catcraft/Video-Player/main/Install/files/config.json'
        r = requests.get(url, allow_redirects=True)
        file_name = os.path.basename(url)
        open(path + "\\" + file_name, 'wb').write(r.content)

def installico(path):
        url = 'https://raw.githubusercontent.com/catcraft/Video-Player/main/Install/files/Logo.ico'
        r = requests.get(url, allow_redirects=True)
        file_name = os.path.basename(url)
        open(path + "\\" + file_name, 'wb').write(r.content)

try:
    #Install the icon from Github
    user_doc = os.path.join(os.path.expanduser("~"), 'Documents\\py')
    py_dir = os.path.join(user_doc, 'logo.ico')
    if os.path.isfile(py_dir) == True:
        os.remove(py_dir)
        installico(user_doc)
    else:
        installico(user_doc)
except:
    pass
    

version = 2.1
modules = ["PyQt5", "tkinter", "pillow", "flask", "threading", "socket", "requests", "pywin32"]

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


def create_shortcut(shortcut_name, shortcut_exe_path, shortcut_icon_path):
    #create a shortcut on the desktop
    user_doc1 = os.path.join(os.path.expanduser("~"), 'Documents\\py')
    py_dir1 = os.path.join(user_doc1, 'logo.ico')
    goal = os.path.join(user_doc1, 'gui.py')

    desktop_path1 = os.path.join(os.path.expanduser("~"), 'Desktop')
    shortcut_name = 'Video Player'
    shortcut_exe_path = goal
    shortcut_icon_path = py_dir1
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(desktop_path1, shortcut_name + ".lnk"))
    shortcut.Targetpath = shortcut_exe_path
    shortcut.IconLocation = shortcut_icon_path
    shortcut.save() 

def download():
    try:
        global download_button
        global txtlabel
        txtlabel.config(text="Downloading...")
        txtlabel.place(relx = 0.43, rely = 0.39)
        download_button.place_forget()
        download_button.config(state='disable')
        root.update()
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents')
        py_dir = os.path.join(user_doc, 'py')
        os.makedirs(py_dir, exist_ok=True)
        progressbar = ttk.Progressbar(root, orient="horizontal", length=294, mode="determinate", maximum=len(modules))
        progressbar.place(rely=0.9)
        progressbar.start()
        for module in modules:
            check_module(module, progressbar)
        
        #create a shortcut on the desktop
        user_doc1 = os.path.join(os.path.expanduser("~"), 'Documents\\py')
        py_dir1 = os.path.join(user_doc1, 'logo.ico')
        goal = os.path.join(user_doc1, 'gui.py')

        desktop_path1 = os.path.join(os.path.expanduser("~"), 'Desktop')
        shortcut_name = 'Video Player'
        shortcut_exe_path = goal
        shortcut_icon_path = py_dir1
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents\\py')
        py_dir = os.path.join(user_doc, 'logo.ico')
        if os.path.isfile(py_dir) == True:
            os.remove(py_dir)
            installico(user_doc)
        else:
            installico(user_doc)
        root.iconbitmap(py_dir)
        root.update()
        #Install the player from Github
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents\\py')
        py_dir = os.path.join(user_doc, 'player.py')
        if os.path.isfile(py_dir) == True:
            os.remove(py_dir)
            installplayer(user_doc)
        else:
            installplayer(user_doc)

        #Install the Background image from Github
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents\\py')
        py_dir = os.path.join(user_doc, 'bg.png')
        if os.path.isfile(py_dir) == True:
            os.remove(py_dir)
            installbg(user_doc)
        else:
            installbg(user_doc)

        #Install the gui file from Github
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents\\py')
        py_dir = os.path.join(user_doc, 'gui.py')
        if os.path.isfile(py_dir) == True:
            os.remove(py_dir)
            installgui(user_doc)
        else:
            installgui(user_doc)

        #Install the Config from Github
        user_doc = os.path.join(os.path.expanduser("~"), 'Documents\\py')
        py_dir = os.path.join(user_doc, 'config.json')
        if os.path.isfile(py_dir) == True:
            os.remove(py_dir)
            installconfig(user_doc)
        else:
            installconfig(user_doc)
        progressbar.stop()


        create_shortcut(shortcut_name, shortcut_exe_path, shortcut_icon_path)
        root.destroy()
        messagebox.showinfo("Installation", "Installed Sucsessfully")

    except Exception as e:
         logging.error(f"Encounterd error during installation of: {e}")
         messagebox.showerror("Error", f"Encounterd error during installation of \n{e}")




if not sys.version:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Python is not installed or version not detected")
    quit()
else:
    print(sys.version)

root = tk.Tk()
root.title("File Downloader")
root.geometry("294x150")
root.config(background="#ffffff")
frame = tk.Canvas(width=294, height=50)
frame.place(relx=0, rely=0.82)
txtlabel = tk.Label(text="Are you sure you whant to install\n Video-PY", font=("Arial", 12), bg="#ffffff")
txtlabel.place(relx = 0.15, rely = 0.3)
download_button = tk.Button(root, width=9,height=1, text="Download", command=download, bg="#ffffff")
download_button.place(rely=0.83, relx=0.4)
try:
    root.iconbitmap(py_dir)
except:
    pass
root.mainloop()