import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from github_integration import upload_to_github  # Ensure these imports are correct
from excel_operations import update_excel  # Ensure these imports are correct

def log_message(message):
    with open("app_log.txt", "a") as log_file:
        log_file.write(f"{message}\n")
    print(message)

def threaded_submit_action():
    try:
        loading_label.grid()  # Show the loading label
        root.update_idletasks()  # Force the GUI to update the loading label visibility
        log_message("Starting the submit action in a new thread")
        submit_action()  # Call the original submit action
    except Exception as e:
        log_message(f"Error in threaded_submit_action: {str(e)}")
    finally:
        loading_label.grid_remove()  # Ensure the loading label is hidden afterwards
        messagebox.showinfo("Success", "Problem added successfully")
        log_message("Submission action completed successfully")
        # Clear all entries after showing success message
        problem_name_entry.delete(0, tk.END)
        problem_code_entry.delete("1.0", tk.END)
        difficulty_level_combo.set("Easy")  # Reset to default or first item
        explanation_entry.delete("1.0", tk.END)
        root.update_idletasks()

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

config_path = get_resource_path("config.txt")

def submit_action():
    try:
        log_message("Reading configuration from config.txt")
        with open(config_path, 'r') as f:
            username, repo_name, repo_folder = [line.strip() for line in f.readlines()]

        problem_name = problem_name_entry.get()
        problem_code = problem_code_entry.get("1.0", tk.END)
        difficulty_level = difficulty_level_var.get()
        explanation = explanation_entry.get("1.0", tk.END)

        if not all([problem_name, problem_code, difficulty_level, explanation.strip()]):
            messagebox.showerror("Error", "All fields are required")
            log_message("Error: Not all fields were filled out")
            return

        loading_label.grid()
        log_message("Preparing to upload problem")

        # Base folder path
        base_folder_path = f"{repo_folder}"
        # Folder path including difficulty level
        folder_path = os.path.join(base_folder_path, difficulty_level.lower())

        # Ensure the base and difficulty level folders exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            log_message(f"Created directory: {folder_path}")

        # Update file_name to include the folder path
        file_name = os.path.join(folder_path, f"{problem_name.replace(' ', '_')}.py")

        with open(file_name, "w") as file:
            file.write(f"\"\"\"\n{explanation}\n\nDifficulty Level: {difficulty_level}\n\"\"\"\n\n{problem_code}")
            log_message(f"Wrote problem to file: {file_name}")

        upload_to_github(file_name, folder_path=repo_folder)
        log_message(f"Uploaded {file_name} to GitHub repository {repo_name}")

        # Update the GitHub link to include the correct path
        code_link = f"https://github.com/{username}/{repo_name}/blob/main/{folder_path.replace(' ', '%20')}/{os.path.basename(file_name).replace(' ', '%20')}"
        update_excel(problem_name, difficulty_level, code_link, explanation, folder_path=repo_folder)
        log_message(f"Updated Excel with problem: {problem_name}")

    except Exception as e:
        log_message(f"Error in submit_action: {str(e)}")

# Set dark theme colors
background_color = '#333333'  # Dark gray
text_color = '#FFFFFF'  # White
button_background = '#555555'  # Darker gray
button_foreground = '#FFFFFF'  # White
entry_background = '#474747'  # Medium dark gray
entry_foreground = '#FFFFFF'  # White

root = tk.Tk()
root.title("LeetCode Problem Submission")
root.geometry("700x500")
root.configure(bg=background_color)
# Improved font style
font_style = ("Arial", 12)
padding = {"padx": (5, 20), "pady": 5}

# Labels and Entries
tk.Label(root, text="Problem Name:", bg=background_color, fg=text_color, font=font_style).grid(row=0, column=0, sticky="w", **padding)
problem_name_entry = tk.Entry(root, font=font_style, bg=entry_background, fg=entry_foreground)
problem_name_entry.grid(row=0, column=1, sticky="ew", **padding)

tk.Label(root, text="Problem Code:", bg=background_color, fg=text_color, font=font_style).grid(row=1, column=0, sticky="w", **padding)
problem_code_entry = tk.Text(root, height=10, font=font_style, bg=entry_background, fg=entry_foreground)
problem_code_entry.grid(row=1, column=1, sticky="ew", **padding)

tk.Label(root, text="Difficulty Level:", bg=background_color, fg=text_color, font=font_style).grid(row=2, column=0, sticky="w", **padding)
difficulty_level_var = tk.StringVar()
difficulty_level_combo = ttk.Combobox(root, textvariable=difficulty_level_var, font=font_style)
difficulty_level_combo['values'] = ('Easy', 'Medium', 'Hard')
difficulty_level_combo.grid(row=2, column=1, sticky="ew", **padding)
difficulty_level_combo.current(0)

tk.Label(root, text="Explanation:", bg=background_color, fg=text_color, font=font_style).grid(row=3, column=0, sticky="w", **padding)
explanation_entry = tk.Text(root, height=5, font=font_style, bg=entry_background, fg=entry_foreground)
explanation_entry.grid(row=3, column=1, sticky="ew", **padding)

submit_button = tk.Button(root, text="Submit", command=lambda: threading.Thread(target=threaded_submit_action).start(), bg=button_background, fg=button_foreground, font=font_style)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Configure grid to ensure widgets expand properly
root.grid_columnconfigure(1, weight=1)

# Centering the Submit button and loading label
submit_button.grid(row=4, column=0, columnspan=2, pady=10)
loading_label = tk.Label(root, text="Please wait, loading...", bg=background_color, fg="#FFD700", font=font_style)
loading_label.grid(row=5, column=0, columnspan=2, pady=10)
loading_label.grid_remove()  # Initially hide the loading label

root.mainloop()
