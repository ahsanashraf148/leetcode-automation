# Upload Leetcode Problems and Solutions to GitHub and Excel

Automatically upload Leetcode problems and your solutions to your GitHub repository and update an Excel sheet with the GitHub file link.

## How to Download

### Method 1: Download ZIP

![alt text](image-4.png)
![alt text](image-5.png)

1. Click on `code` then `Download Zip`.
2. Extract the zip file and open the folder.

### Method 2: Clone The Repository

![alt text](image-4.png)
![alt text](image-6.png)

1. Click on `code`
2. Copy the web URL
3. Open Gitbash on any folder you want to clone the repository in and paste

```shell
    git clone {url you copied} .
```

## How to Use

### Setup Git and GitHub Repositories

1. Click on `Setup Git and Github Repositories`.
2. Enter your `github username`.
3. Enter the desired repository name.
4. Enter your `GitHub Token`.
5. Create a new folder for your code files and enter its path.
6. Click on `Create and Push Repo`.

![Setup Instructions](image.png)
![Setup Form](image-1.png)

### Upload Problem to GitHub

1. Go back to the main window.
2. Click on `Upload Problem To Github`.
3. Enter the `Problem name`.
4. Select `Difficulty Level`.
5. Enter the `problem code` and its `explanation`.
6. Click `Submit`.

![Upload Problem](image-2.png)
![Problem Form](image-3.png)

**Congratulations!** The problem file has been created in the specified folder, uploaded to GitHub, and its details appended to `problems.xlsx`.

## Prerequisites

- Python must be installed.

## Getting a GitHub Token

1. **Log in to GitHub:** Open your web browser and log in to your GitHub account.
2. **Access Settings:** Click on your profile picture, then select `Settings`.
3. **Developer Settings:** Scroll down and click on "Developer settings".
4. **Personal Access Tokens:** Click on "Personal access tokens".
5. **Generate New Token:** Click on "Generate new token".
6. **Token Description:** Enter a description for your token.
7. **Select Scopes:** Choose the necessary scopes under the "repo" category.
8. **Generate Token:** Click "Generate token" at the bottom.
9. **Copy Your New Token:** Copy your new token immediately. You won’t be able to see it again!

**Important:** Treat your token as a password. Keep it secure and do not share it.
