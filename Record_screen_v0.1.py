import pyautogui
import numpy as np
import cv2
import time
import datetime
import tkinter as tk
import threading
import win32con
import win32api

def start_recording():
    global result, start_time, recording

    # Get list of connected screens and their resolutions
    screen_list = []
    for i in range(win32api.GetSystemMetrics(win32con.SM_CMONITORS)):
        left, top, right, bottom = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors(None, None)[i][0])["Monitor"]
        screen_list.append({"id": i, "resolution": (right - left, bottom - top)})

    # Prompt user to select a screen to record
    print("Select the screen you want to record:")
    for i, screen in enumerate(screen_list):
        print(f"{i+1}. {screen['resolution'][0]}x{screen['resolution'][1]}")
    selected_screen = int(input()) - 1
    screen_width, screen_height = screen_list[selected_screen]['resolution']
    # Set codec for video file
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    # Get current date and time
    now = datetime.datetime.now()

    # Create unique file name based on current date and time
    file_name = now.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"

    # Create VideoWriter object
    result = cv2.VideoWriter(file_name, fourcc, 15.0, (screen_width, screen_height))

    # Get start time
    start_time = time.time()
    recording = True
    while recording:
        # Take screenshot of screen
        img = pyautogui.screenshot(region=(left, top, right, bottom))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result.write(frame)

    # Release and save video file
    result.release()
    print(f"Screen recording saved as {file_name}")


def stop_recording():
    global recording
    recording = False

def start():
    threading.Thread(target=start_recording).start()

# Create a flag to check if recording should stop
recording = False

# Create a tkinter window
root = tk.Tk()
root.title("Screen Recorder")

# Create start and stop buttons
start_button = tk.Button(root, text="Start Recording", command=start)
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)

# Pack buttons into the window
start_button.pack()
stop_button.pack()

root.mainloop()
