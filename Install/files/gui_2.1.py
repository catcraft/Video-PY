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
from flask import Flask, request, redirect
import threading
import socket

# Add a new global variable to store the path of the file where the video info will be saved
col1 = "#a9b7cc"
topcol = "#293241"
bgcol = "#98c1d9"
hlpbg = "#7b9bb1"
btncol = "#ababab"
version = 0
small = False
try:
    name = (platform.uname().node)
    if name == "PHNAGSF2211":
        small = True
except:
    print("no name detected continuing")

VIDEOS_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'saved_data.txt')
PLAYER_FILE_PATH= os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'player.py')
BG_FILE_PATH= os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'bg.png')
CONFIG_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Py', 'config.json')

ip_address = socket.gethostbyname(socket.gethostname())
print(ip_address)
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
                exec(f'button{number}.config(bg=f"white")')
                button_processes[number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(number), file_path])
            else:
                exec(f"button{number}.configure(bg=btncol)")
                print(number)
                print(file_path)
                button_processes[number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(number), file_path])
                print(button_processes)
        return redirect('/')
    mp4_files = [f for f in os.listdir(video_drive) if f.endswith('.mp4')]
    return """
       <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="apple-mobile-web-app-title" content="Web Gui Video">
            <meta name="apple-mobile-web-app-status-bar-style" content="black">
            <link href="https://fonts.googleapis.com/css2?family=SF+Pro&display=swap" rel="stylesheet">
        </head>

        <div style="display: flex; justify-content: left; align-items: left; background: linear-gradient(135deg, #007ACC 0%, #00C9FF 100%);">
        <a style="margin-left: 0px; margin-top: 17px; ">
            <img src="https://iili.io/HRaHi5N.png" border="0" style="height: 61px; width: 86.4x"/>
        </a>
        <form method="POST" style="margin-right: 10px;">
            <button type="submit" name="button"  value="Random" style="border-radius: 10px; margin-top: 20px;  border: 1px solid white; height: 75px; windth: 150px; padding-left: 15px; padding-right: 15px;">Random</button>
        </form>
        <form method="POST" style="margin-left: 5px;">
            <button type="submit" name="button" value="Kill Running" style="border-radius: 10px; margin-top: 20px; border: 1px solid white;height: 75px; windth: 150px">Kill Running</button>
        </form>
        </div>

        <div style="background-color: #E5E5E5; padding: 5px;">
        <form method="POST" style="margin-left: 20px; margin-top: 20px;">
            <label style="font-family: 'SF Pro', sans-serif; font-weight: bold; ">Video:</label>
            <select name="file" style="border-radius: 25px; background-color: #CCCCCC; color: #ffffff; border: none; font-family: 'SF Pro', sans-serif; padding-top: 10px; padding-bottom: 20px; font-weight: bold; -webkit-appearance: none; padding-left:30">
            {}
            </select>
        </div>
        <div style="background-color: #E5E5E5; padding: 5px;margin-top: 50px; display: flex; justify-content: space-between;">
            <label style=" font-family: 'SF Pro', sans-serif; padding-top: 10px; font-weight: bold;">Bildschirm:</label>
            <select name="number" style="border-radius: 25px; background-color: #CCCCCC; color: #ffffff; border: none; font-family: 'SF Pro', sans-serif; padding-top: 10px; padding-bottom: 10px; font-weight: bold; -webkit-appearance: none; padding-left:30; padding-right:30">
                {}
            </select>
            <button type="submit" style="border-radius: 10px; border: 1px solid white; font-size: 20px;" name="button" -webkit-appearance: none;>Open</button>
        </div>

                
    """.format('\n'.join('<option value="{}">{}</option>'.format(f, f) for f in mp4_files), '\n'.join('<option value="{}">{}</option>'.format(i, i) for i in range(1, number_of_monitors + 1)))

def start_flask():
    app.run(host=(str(ip_address)), port=5000)

# Get the current screen width and height
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
number_of_monitors = user32.GetSystemMetrics(80)

# Calculate the button size based on the screen width
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

try:
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = json.load(f)
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    config = {'video_drive': 'D:\\', 'version': '1.0'}

version = config['version']
video_drive = (config['video_drive'] + "\\")



# Create a dictionary to store the process for each button
button_processes = {}
playing_videos = []
# Create the main window
window = tk.Tk()
window.geometry(f"{screen_width}x{screen_height}")
window.config(bg=bgcol)
window.title('Video by Eric')



# Get the current screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Load the image and resize it to the screen dimensions
image = Image.open(BG_FILE_PATH)
image = image.point(lambda p: p * 0.3)
image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

# Create a PhotoImage object from the image
image = ImageTk.PhotoImage(image)

# Create a label widget with the image as the background
label = tk.Label(window, image=image)

# Place the label widget at the top of the window
label.pack(side="top", fill="both", expand=True)

#  Define a function to be called when a button is clicked
def button_clicked(number, show_file_dialog):
    print(number)
    # Check if the button has a process running
    if number in button_processes:
        # If it does, kill the process
        button_processes[number].kill()
        # Remove the process from the dictionary
        del button_processes[number]
        exec(f'button{number}.config(bg=f"white")')
    # If the show_file_dialog argument is True, show the file selection dialog
    if show_file_dialog:
        file_path = filedialog.askopenfilename()
        # If a file was selected, start a new process
        exec(f"button{number}.configure(bg=btncol)")
        if file_path:
            print("function clicked number:", number)
            print(file_path)
            button_processes[number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(number), file_path])

            
def on_closing():
    # Terminate all subprocesses
    for number, process in button_processes.items():
        process.terminate()
        
    # Save the current state of the video player to a file in JSON format
    with open(VIDEOS_FILE_PATH, "w") as file:
        # Create a dictionary to store the data
        data = {}
        # Add the list of processes to the data dictionary
        data["processes"] = {number: {"file_path": process.args[3], "screen_number": number} for number, process in button_processes.items()}
        # Write the data to the file as a JSON string
        file.write(json.dumps(data))
    # Close the app
    window.destroy()
    subprocess.Popen('taskkill /im /f python.exe', shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    os._exit(0)

    
def random_starter():
    killall()
    for i in range(1, (number_of_monitors + 1)):
        z = i - 1
        start_random_video((z))
        print("starting video count, ", z)
    playing_videos.clear()
    for i in range(number_of_monitors):
                exec(f'button{i + 1}.config(bg=btncol)')

def killall():
    # Get a list of all the running processes
    processes = [p for p in button_processes.values()]

    # Kill all the processes
    for process in processes:
        process.kill()

    # Clear the button_processes dictionary
    button_processes.clear()
    for i in range(number_of_monitors):
                exec(f'button{i+1}.config(bg=f"white")')

def start_random_video(number):
    found = 0
    # Get a list of all the video files in D:\
    files = [f for f in os.listdir(video_drive) if f.endswith(".mp4") or f.endswith(".avi")]
    # Select a random file from the list
    while found == 0:
        file = random.choice(files)
        # Start the video on the specified screen
        file = random.choice(files)
        if file not in playing_videos:
            print("Found a video, screen: ", number)
            button_processes[number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(number), f"D:\\{file}"])
            playing_videos.append(file)
            found = 1

def helppopup():
    tkinter.messagebox.showinfo("Steuerung",  "Zum Schliessen von Videos: Rechtsklick auf den zuvor ausgewählten Bildschirm")


top_bar = tk.Frame(window, bg=topcol, width=screen_width, height=bar_size)
top_bar.place(x = 0, y = 0)

ip_label = tk.Label(window, text=f"{ip_address}:5000", font=("Helvetica", int(font_size / 1.5)), bg="black", fg="white")



startx = 0.1
for i in range(number_of_monitors):
    exec(f'button{i+1} = tk.Button(window, text=f"{i+1}",  width=w, height=h, font=("Helvetica", sz, "bold"), relief="solid", bd=4, command=lambda: button_clicked({i + 1}, True))')
    exec(f'button{i+1}.place(relx = startx, rely = 0.5)')
    exec(f'button{i+1}.bind("<Button-3>", lambda event: button_clicked({i + 1}, False))')
    startx = startx + 0.2
exec(f'button{number_of_monitors + 1} = tk.Button(text="Hilfe", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=lambda:helppopup(), bg = hlpbg)')
exec(f'button{number_of_monitors+1}.place(relx = 0, rely = 0)')
exec(f'button{number_of_monitors + 2} = tk.Button(text="Hilfe", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=lambda:helppopup(), bg = hlpbg)')
exec(f'button{number_of_monitors+2}.place(relx = 0, rely = 0)')
buttonrnd = tk.Button(text="Zufällig", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=lambda: random_starter())
buttonend = tk.Button(text="Alle Stoppen", width=w, height=int(h / 2), font=("Helvetica", int(sz / 2), "bold"), relief="solid", bd=4, command=lambda: killall())
buttonrnd.place(relx = 0.10, rely=0)
buttonend.place(relx = 0.2, rely=0)



# Place the label at the bottom right corner of the window
ip_label.place(relx=0.86, rely=0.91)

# Bind the right mouse button click event to the button_clicked function
# Add the buttons to the window
# Check if the videos file exists and is not empty
if os.path.exists(VIDEOS_FILE_PATH) and os.path.getsize(VIDEOS_FILE_PATH) > 0:
    # Open the file and read the data from it
    with open(VIDEOS_FILE_PATH, "r") as file:
        data = json.loads(file.read())
        # Get the list of processes from the data
        processes = data["processes"]
        # Start each process again
        for process_info in processes.values():
            file_path = process_info["file_path"]
            screen_number = process_info["screen_number"]
            button_processes[screen_number] = subprocess.Popen([sys.executable, PLAYER_FILE_PATH, str(screen_number), file_path])
            for i in range(number_of_monitors):
                exec(f'button{i+1}.config(bg=btncol)')
   

# Set the app to call the on_closing function when closed
window.protocol("WM_DELETE_WINDOW", on_closing)
label = tk.Label(text=f"GUI {version} Made with ❤️ by Eric & ChatGPT", font=("Segoe UI Emoji", int(font_size / 1.5)), bg="black", fg="White")
label.place(relx=0.01, rely=0.91)

window.state("zoomed")
# Run the Tkinter event loop
flask_thread = threading.Thread(target=start_flask)
flask_thread.start()
window.mainloop()