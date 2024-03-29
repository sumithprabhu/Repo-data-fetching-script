import subprocess
from datetime import datetime, timedelta
import shutil
import os

# Path to your local git repository
repo_path = "/home/sumith/Desktop/Workspace/push-website/"
# Path to the local directory where you want to store/update the files
local_training_data_dir = "/home/sumith/Desktop/Workspace/Automate-data-fetching/Changing_files_with_changes/Storage/"

def get_date_7_days_ago():
    """Calculate the date for 7 days ago."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    return seven_days_ago.strftime('%Y-%m-%d')

def list_changed_files_in_past_week(repo_path):
    """List names of files changed from 7 days ago to today, explicitly on the main branch."""
    date_7_days_ago = get_date_7_days_ago()
    # Explicitly specifying the branch now
    branch = "main"
    
    # Constructing the git log command to get changes from 7 days ago
    command = [
        "git", "-C", repo_path, "log", branch, "--name-only", "--since", date_7_days_ago, "--pretty=format:", "--", "docs"
    ]
    
    # Execute the git log command
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:  # Successfully executed command
        if result.stdout:
            changed_files = set(filter(None, result.stdout.strip().split('\n')))
            if changed_files:
                print(f"Files changed from 7 days ago ({date_7_days_ago}) to today in the {branch} branch:")
                for file in changed_files:
                    print(file)
            else:
                print(f"No changes detected from 7 days ago ({date_7_days_ago}) to today in the {branch} branch.")
        else:
            print(f"No changes detected from 7 days ago ({date_7_days_ago}) to today in the {branch} branch.")
    else:
        print("Error executing git command:", result.stderr)

def update_local_file(repo_path, file_path, local_dir):
    """Update or add the file in the local directory based on the repository."""
    source_path = os.path.join(repo_path, file_path)
    destination_path = os.path.join(local_dir, os.path.basename(file_path))
    
    # Check if the file exists in the local directory
    if os.path.exists(destination_path):
        print(f"Updating: {os.path.basename(file_path)}")
    else:
        print(f"Adding: {os.path.basename(file_path)}")
    
    # Copy or update the file
    shutil.copy2(source_path, destination_path)

if __name__ == "__main__":
    list_changed_files_in_past_week(repo_path)
