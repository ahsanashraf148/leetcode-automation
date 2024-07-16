import tkinter as tk
from subprocess import Popen, PIPE

def run_setup():
    install_requirements()
    Popen(["python", "setup.py"], stdout=PIPE, stderr=PIPE)

def run_main_app():
    process = Popen(["python", "main_app.py"], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()  # Wait for the process to finish and get the output and error
    print("Output:", output.decode())  # Decode from bytes to string and print
    print("Error:", error.decode())  

def install_requirements():
    Popen(["python", "-m", "pip", "install", "-r", "requirements.txt"], stdout=PIPE, stderr=PIPE)

# Set dark theme colors
background_color = '#333333'  # Dark gray
text_color = '#FFFFFF'  # White
button_background = '#555555'  # Darker gray
button_foreground = '#FFFFFF'  # White

root = tk.Tk()
root.title("GitHub Automation Tool")
root.geometry("700x300")
root.configure(bg=background_color)
root.iconbitmap('icon.ico')

# Improved font style
font_style = ("Arial", 12)
padding = {"padx": 20, "pady": 10}

install_requirements()

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