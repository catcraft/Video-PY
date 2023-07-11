import tkinter as tk
from tkinter import *
import subprocess
import sys
import ctypes
import tkinter.messagebox
from tkinter import filedialog
import os, platform
import json
from PIL import Image, ImageTk
import random
from flask import Flask, request, redirect, render_template
import threading
import socket
from datetime import datetime
import tkinter.messagebox as messagebox
from PIL import Image
# Add a new global variable to store the path of the file where the video info will be saved
CONFIG_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'config.json')
try:
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = json.load(f)
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    config = {'video_drive': 'D:\\', 'version': '1.0'}

#Colors
col1 = "#a9b7cc"
topcol = "#293241"
bgcol = "#98c1d9"
hlpbg = "#7b9bb1"
btncol = "#ababab"
small = False

#Monitor Stuff
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
number_of_monitors = user32.GetSystemMetrics(80)

#Sizes
#I hate this but i have to do it
try:
    name = (platform.uname().node)
    if name == "PHNAGSF2211":
        small = True
except:
    print("no name detected continuing")

if not small:
    button_size = screen_width // 100
    font_size = screen_height // 40
    bar_size = screen_height // 10
else:
    button_size = screen_width // 120
    font_size = screen_height // 60
    bar_size = screen_height // 15

w = int(button_size)
h = int(button_size / 3)
sz = int(font_size)

version = config['version']
video_drive = (config['video_drive'] + "\\")
button_processes = {}
playing_videos = []
ip_address = socket.gethostbyname(socket.gethostname())

button_list = []  # Create an empty list to store the buttons
VIDEOS_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'saved_data.txt')
PLAYER_FILE_PATH= os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'player.py')
BG_FILE_PATH= os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'bg.png')
MINMAX_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'Minmax.png')
SHWONUM_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'ShowNum.py')
SHWONUM_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'ShowNum.py')


#Flask
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['button'] == 'Random':
            random_starter()
        elif request.form['button'] == 'Kill Running':
            killall()
        else:
            file_name = request.form['file']
            file_path = os.path.join(video_drive, file_name)
            number = int(request.form['number'])
            if number in button_processes:
                # If it does, kill the process
                button_processes[number].kill()
                # Remove the process from the dictionary
                del button_processes[number]
                button_list[number-1].config(bg='white')
            button_list[number-1].configure(bg=btncol)
            button_processes[number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(number), file_path])  
        return redirect('/')
    mp4_files = [f for f in os.listdir(video_drive) if f.endswith('.mp4')]
    return render_template('index.html', mp4_files=mp4_files, number_of_monitors=number_of_monitors)

def start_flask():
    app.run(host="0.0.0.0", port=5069)

#Tkinter GUI
window = tk.Tk()

def button_clicked(number, show_file_dialog):
    if number in button_processes:
        button_processes[number].kill()
        del button_processes[number]
        button_list[number-1].config(bg='white')
    if show_file_dialog:
        file_path = filedialog.askopenfilename()
        if file_path:
            button_list[number-1].configure(bg=btncol)
            button_processes[number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(number), file_path])

def on_closing():
    for number, process in button_processes.items():
        process.terminate()
    with open(VIDEOS_FILE_PATH, "w") as file:
        data = {}
        data["processes"] = {number: {"file_path": process.args[3], "screen_number": number} for number, process in button_processes.items()}
        file.write(json.dumps(data))
    window.destroy()
    subprocess.Popen('taskkill /im /f python.exe', shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    os._exit(0)

    
def random_starter():
    try:
        files = [f for f in os.listdir(video_drive) if f.endswith(".mp4") or f.endswith(".avi")]
    except:
        messagebox.showerror("File Error", f"Could not find the files in {str(video_drive)}")
        return
    killall()
    playing_videos.clear()

    for i in range(number_of_monitors):
        selected_file = None
        while not selected_file:
            available_files = [file for file in files if file not in playing_videos]
            if available_files:
                selected_file = random.choice(available_files)
        file_path = os.path.join(video_drive, selected_file)
        button_processes[i] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(i), file_path])
        playing_videos.append(selected_file)

    for button in button_list:
        button.config(bg=btncol)


def killall():
    for process in button_processes.values():
        process.kill()
    button_processes.clear()
    for button in button_list:
        button.config(bg='white')

if os.path.exists(VIDEOS_FILE_PATH) and os.path.getsize(VIDEOS_FILE_PATH) > 0:
    with open(VIDEOS_FILE_PATH, "r") as file:
        data = json.loads(file.read())
        processes = data["processes"]
        for process_info in processes.values():
            file_path = process_info["file_path"]
            screen_number = process_info["screen_number"]
            button_processes[screen_number] = subprocess.Popen(
                [sys.executable, PLAYER_FILE_PATH, str(screen_number), file_path]
            )
            
            for i in range(number_of_monitors):
                button = button_list[i]
                button.config(bg=btncol)
                
def helppopup():
    tkinter.messagebox.showinfo("Steuerung",  "Zum Schliessen von Videos: Rechtsklick auf den zuvor ausgewählten Bildschirm")

#Background image
#Why a label tho.......
image = Image.open(BG_FILE_PATH)
image = image.point(lambda p: p * 0.3)
image = image.resize((screen_width + 20, screen_height + 20), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(image)
label = tk.Label(window, image=image)
label.place(x=-10,y=-10)

#Frame for Screens
frame = tk.Frame(window)
frame.place(relx=0.5, rely=0.5, anchor="center")
for i in range(number_of_monitors):
    button = tk.Button(frame, text=f"{i+1}", width=w, height=h, font=("Helvetica", sz, "bold"), relief="solid", bd=4)
    button.grid(column=i, row=0)
    button.bind("<Button-1>", lambda event, idx=i+1: button_clicked(idx, True))
    button.bind("<Button-3>", lambda event, idx=i+1: button_clicked(idx, False))
    button_list.append(button)  # Add the button to the list

#Main Buttons
timelabel = tk.Label(text="00:00:00", bg=topcol, font=("small fonts", int(sz * 1.3), "bold"), fg="white")
timelabel.place(relx=0.47, rely=0)

helpbutton = tk.Button(text="Hilfe", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=helppopup, bg=hlpbg)
helpbutton.place(relx=0, rely=0)

buttonrnd = tk.Button(text="Zufällig", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=random_starter)
buttonrnd.place(relx=0.84, rely=0)

buttonend = tk.Button(text="Alle Stoppen", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=killall)
buttonend.place(relx=0.92, rely=0)

label = tk.Label(text=f"GUI {version} Made with ❤️ by Eric & ChatGPT", font=("Segoe UI Emoji", int(font_size / 1.5)), bg="black", fg="White")
label.place(relx=0.01, rely=0.96)

ip_label = tk.Label(window, text=f"{ip_address}:5000", font=("Helvetica", int(font_size / 1.5)), bg="black", fg="white")
ip_label.place(relx=0.94, rely=0.96)

#Clock
def updatetime():
    currentDateAndTime = datetime.now()
    time = currentDateAndTime.strftime("%H:%M:%S")
    timelabel.config(text=time, font=("small fonts", (int(sz * 1.3))))
    window.after(1000, updatetime)
updatetime()

window.title('Video by Eric')
window.protocol("WM_DELETE_WINDOW", on_closing)      
window.attributes("-fullscreen", True)
flask_thread = threading.Thread(target=start_flask)
flask_thread.start()
window.mainloop()
