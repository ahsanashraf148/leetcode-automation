import os
import sys
import time
import tkinter as tk

from subprocess import Popen, PIPE

def install_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    process = Popen(["python", "-m", "pip", "install", "-r", requirements_path], stdout=PIPE, stderr=PIPE)
    process.wait()
    print("Installing requirements", end="")
    while process.poll() is None:
        print(".", end="")
        sys.stdout.flush()  # Ensure the dot is printed immediately
        time.sleep(1)  # Wait a bit before printing the next dot
    output, error = process.communicate()  # Wait for the installation to complete
    if error:
        print("Error installing requirements:", error.decode())
    else:
        print("Requirements installed successfully")

def run_setup():
    install_requirements()
    process = Popen(["python", "code/setup.py"], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    print("Output:", output.decode())
    print("Error:", error.decode())  

def run_main_app():
    process = Popen(["python", "code/main_app.py"], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    print("Output:", output.decode())
    print("Error:", error.decode())  


# Set dark theme colors
background_color = '#333333'  # Dark gray
text_color = '#FFFFFF'  # White
button_background = '#555555'  # Darker gray
button_foreground = '#FFFFFF'  # White


root = tk.Tk()
root.title("GitHub Automation Tool")
root.geometry("700x300")
root.configure(bg=background_color)
root.iconbitmap('code/icon.ico')

font_style = ("Arial", 12)
padding = {"padx": 20, "pady": 10}

heading_label = tk.Label(root, text="GitHub Automation Tool", bg=background_color, fg="#FFD700", font=("Arial", 16, "bold"))
heading_label.pack(pady=(20, 10))

# Setup Button
setup_button = tk.Button(root, text="Setup Git & GitHub Repositories", command=run_setup, bg=button_background, fg=button_foreground, font=font_style)
setup_button.pack(pady=10, padx=20, fill=tk.X)

# Main App Button
main_app_button = tk.Button(root, text="Upload Problem to GitHub", command=run_main_app, bg=button_background, fg=button_foreground, font=font_style)
main_app_button.pack(pady=10, padx=20, fill=tk.X)

instruction_label = tk.Label(root, text="Please read the README.md on GitHub before using this tool.\nRefer to it if anything seems confusing.\nAlso Setup is only required only once, click UPLOAD PROBLEM ON GITHUB\n to upload problems everytime", bg=background_color, fg="#FFD700", font=("Arial", 10, "italic"))
instruction_label.pack(pady=(10, 20))

root.mainloop()