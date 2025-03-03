from github import Github
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

repo_owner = os.getenv("OWNER")
repo_name = os.getenv("REPO")
pat = os.getenv("PAT")

clone_directory = "bot"

g = Github(pat) if pat else Github()
pat = pat if pat else repo_owner

repo = g.get_user(repo_owner).get_repo(repo_name)
clone_url = repo.clone_url
subprocess.run(["git", "pull", f"https://{pat}@github.com/{repo_owner}/{repo_name}"])
subprocess.run(["python3", "bot/main.py"])