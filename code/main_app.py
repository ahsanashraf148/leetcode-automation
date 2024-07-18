import os
import tkinter as tk
from tkinter import messagebox, ttk

from github_integration import upload_to_github
from excel_operations import update_excel

def submit_action():
    with open('config.txt', 'r') as f:
        username, repo_name, repo_folder = [line.strip() for line in f.readlines()]
    problem_name = problem_name_entry.get()
    problem_code = problem_code_entry.get("1.0", tk.END)
    difficulty_level = difficulty_level_var.get()
    explanation = explanation_entry.get("1.0", tk.END)

    if not all([problem_name, problem_code, difficulty_level, explanation.strip()]):
        messagebox.showerror("Error", "All fields are required")
        return

    # Base folder path
    base_folder_path = f"{repo_folder}"
    # Folder path including difficulty level
    folder_path = os.path.join(base_folder_path, difficulty_level.lower())

    # Ensure the base and difficulty level folders exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Update file_name to include the folder path
    file_name = os.path.join(folder_path, f"{problem_name.replace(' ', '_')}.py")
    
    with open(file_name, "w") as file:
        file.write(f"\"\"\"\n{explanation}\n\nDifficulty Level: {difficulty_level}\n\"\"\"\n\n{problem_code}")

    upload_to_github(file_name, folder_path=repo_folder)

    # Update the GitHub link to include the correct path
    code_link = f"https://github.com/a{username}/{repo_name}/blob/main/{folder_path.replace(' ', '%20')}/{file_name.replace(' ', '%20')}"
    update_excel(problem_name, difficulty_level, code_link, explanation, folder_path=repo_folder)

    messagebox.showinfo("Success", "Problem added successfully")
    # Clear all entries after showing success message
    problem_name_entry.delete(0, tk.END)
    problem_code_entry.delete("1.0", tk.END)
    difficulty_level_combo.set("Easy")  # Reset to default or first item
    explanation_entry.delete("1.0", tk.END)

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
root.iconbitmap('code/icon.ico')
# Improved font style
font_style = ("Arial", 12)
padding = {"padx": (5, 20), "pady": 5}


# Labels and Entries
tk.Label(root, text="Problem Name:", bg=background_color, fg=text_color, font=font_style).grid(row=0, column=0, sticky="w", **padding)
problem_name_entry = tk.Entry(root, font=font_style, bg=entry_background, fg=entry_foreground)
problem_name_entry.grid(row=0, column=1, sticky="ew", **padding)

tk.Label(root, text="Difficulty Level:", bg=background_color, fg=text_color, font=font_style).grid(row=1, column=0, sticky="w", **padding)
difficulty_level_var = tk.StringVar()
difficulty_level_combo = ttk.Combobox(root, textvariable=difficulty_level_var, font=font_style, state="readonly")
difficulty_level_combo['values'] = ("Easy", "Medium", "Hard")
difficulty_level_combo.grid(row=1, column=1, sticky="ew", **padding)
difficulty_level_combo.current(0)

tk.Label(root, text="Problem Code:", bg=background_color, fg=text_color, font=font_style).grid(row=2, column=0, sticky="nw", **padding)
problem_code_entry = tk.Text(root, height=10, font=font_style, bg=entry_background, fg=entry_foreground)
problem_code_entry.grid(row=2, column=1, sticky="ew", **padding)

tk.Label(root, text="Explanation:", bg=background_color, fg=text_color, font=font_style).grid(row=3, column=0, sticky="nw", **padding)
explanation_entry = tk.Text(root, height=10, font=font_style, bg=entry_background, fg=entry_foreground)
explanation_entry.grid(row=3, column=1, sticky="ew", **padding)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit_action, bg=button_background, fg=button_foreground, font=font_style)
submit_button.grid(row=4, column=0, columnspan=2, sticky="ew", **padding)

# Grid column configuration for resizing
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

root.mainloop()