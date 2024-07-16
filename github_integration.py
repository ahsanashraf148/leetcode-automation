import subprocess
import os

def upload_to_github(file_name, folder_path):
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
        # Attempt to push, and set upstream if needed
        subprocess.run(["git", "push", "--set-upstream", "origin", "master"], check=True, cwd=folder_path)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to upload {file_name} to GitHub from {folder_path}: {e}")