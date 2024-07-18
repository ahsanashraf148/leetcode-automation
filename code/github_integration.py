import subprocess
import os

def upload_to_github(file_name, folder_path):
    # Check for Git installation
    try:
        subprocess.run(["git", "--version"], check=True)
    except subprocess.CalledProcessError:
        print("Git is not installed on this system.")
        return

    # Check if the specified folder is a Git repository
    if not os.path.isdir(os.path.join(folder_path, ".git")):
        print("The specified folder is not a Git repository.")
        return

    try:
        # Add the file to staging
        subprocess.run(["git", "add", file_name], check=True, cwd=folder_path)
        
        # Check if there are changes to commit
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=folder_path)
        if status_result.stdout.strip() == "":
            print("No changes to commit.")
            return
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", f"Add {file_name}"], check=True, cwd=folder_path)
        
        # Verify if 'origin' remote is set up
        remote_result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, cwd=folder_path)
        if remote_result.returncode != 0:
            print("Remote 'origin' is not set up. Please set it up before pushing.")
            return
        
        # Get the current branch name
        current_branch_result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=folder_path)
        current_branch = current_branch_result.stdout.strip()
        
        # Attempt to push, and set upstream if needed
        subprocess.run(["git", "push", "--set-upstream", "origin", current_branch], check=True, cwd=folder_path)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")