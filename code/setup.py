import os
import subprocess
import requests
import tkinter as tk
from tkinter import messagebox

def log_message(message):
    with open("setup_log.txt", "a") as log_file:
        log_file.write(f"{message}\n")
    print(message)

# Set dark theme colors
background_color = '#333333'  # Dark gray
text_color = '#FFFFFF'  # White
button_background = '#555555'  # Darker gray
button_foreground = '#FFFFFF'  # White
entry_background = '#474747'  # Medium dark gray
entry_foreground = '#FFFFFF'  # White

def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        error_message = f"Error: {stderr.decode('utf-8')}"
        log_message(error_message)
        return ""
    else:
        return stdout.decode('utf-8').strip()

def initialize_local_git_repo(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        log_message(f"Created directory: {folder_path}")
    run_command("git init", cwd=folder_path)
    log_message("Initialized local Git repository")

def create_github_repo(username, repo_name, token):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "name": repo_name,
        "private": False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        log_message("GitHub repository created successfully")
        return response.json()["clone_url"]
    else:
        error_message = f"Failed to create GitHub repository. Response: {response.json()}"
        log_message(error_message)
        return None

def push_to_github(username, repo_name, folder_path):
    run_command("git fetch", cwd=folder_path)
    branch_name = run_command("git branch --show-current", cwd=folder_path).strip()
    if not branch_name:
        error_message = "Error: Could not determine the current branch name. Defaulting to 'main'."
        log_message(error_message)
        branch_name = "main"
    
    run_command(f"git remote add origin https://github.com/{username}/{repo_name}.git", cwd=folder_path)
    run_command("git add .", cwd=folder_path)
    
    commit_result = run_command('git commit -m "Initial commit"', cwd=folder_path)
    if "nothing to commit" in commit_result:
        log_message("Warning: Nothing to commit, proceeding to push.")
    
    push_result = run_command(f"git push -u origin {branch_name}", cwd=folder_path)
    if "error" in push_result or "failed" in push_result:
        error_message = f"Error while pushing to GitHub: {push_result}"
        log_message(error_message)
    else:
        log_message("Pushed to GitHub successfully")

def gui_main():
    window = tk.Tk()
    window.title("GitHub Repo Creator")
    window.configure(bg=background_color)
    window.geometry("700x500")

    font_style = ("Arial", 12)
    padding = {"padx": (5, 20), "pady": 5}

    tk.Label(window, text="GitHub Username:", bg=background_color, fg=text_color, font=font_style).pack(pady=(10, 0))
    username_entry = tk.Entry(window, font=font_style, bg=entry_background, fg=entry_foreground)
    username_entry.pack(fill=tk.X, padx=20)

    tk.Label(window, text="Repository Name:", bg=background_color, fg=text_color, font=font_style).pack()
    repo_name_entry = tk.Entry(window, font=font_style, bg=entry_background, fg=entry_foreground)
    repo_name_entry.pack(fill=tk.X, padx=20)

    tk.Label(window, text="GitHub Token:", bg=background_color, fg=text_color, font=font_style).pack()
    token_entry = tk.Entry(window, show="*", font=font_style, bg=entry_background, fg=entry_foreground)
    token_entry.pack(fill=tk.X, padx=20)

    tk.Label(window, text="Folder Path:", bg=background_color, fg=text_color, font=font_style).pack()
    folder_path_entry = tk.Entry(window, font=font_style, bg=entry_background, fg=entry_foreground)
    folder_path_entry.pack(fill=tk.X, padx=20)

    def on_submit():
        global USERNAME, REPO_NAME, FOLDER_PATH  
        USERNAME = username_entry.get()
        REPO_NAME = repo_name_entry.get()
        token = token_entry.get()
        FOLDER_PATH = folder_path_entry.get()
        
        log_message("Starting repository setup process")
        initialize_local_git_repo(FOLDER_PATH)
        repo_url = create_github_repo(USERNAME, REPO_NAME, token)
        if repo_url:
            push_to_github(USERNAME, REPO_NAME, FOLDER_PATH)
            log_message(f"Repository {REPO_NAME} has been successfully pushed to GitHub")
            messagebox.showinfo("Success", f"Repository {REPO_NAME} has been successfully pushed to GitHub.", parent=window)
            window.destroy()
        else:
            log_message(f"Failed to push the repository {REPO_NAME} to GitHub")
            messagebox.showerror("Error", "Failed to push the repository to GitHub.", parent=window)
        
        with open('config.txt', 'w') as f:
            f.write(f"{USERNAME}\n{REPO_NAME}\n{FOLDER_PATH}")
        log_message("Configuration saved to config.txt")

    submit_button = tk.Button(window, text="Create and Push Repo", command=on_submit, bg=button_background, fg=button_foreground, font=font_style)
    submit_button.pack(fill=tk.X, padx=20, pady=10)

    window.mainloop()

if __name__ == "__main__":
    gui_main()
