import subprocess
from datetime import datetime, timedelta
import shutil
import os
import requests

# Paths configuration
repo_path = "/home/sumith/Desktop/Workspace/Demo/"
local_training_data_dir = "/home/sumith/Desktop/Workspace/Automate-data-fetching/Changing_files_with_changes/Training_data"
storage_dir_path = "/home/ubuntu/push-ai-chat/ai-python-code/storage"
training_script_path = "/home/ubuntu/push-ai-chat/ai-python-code/training.py"


def git_pull(repo_path):
    """Pull the latest changes from the remote repository."""
    print("Pulling latest changes from the remote repository...")
    command = ["git", "-C", repo_path, "pull", "origin", "main"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Successfully pulled the latest changes.")
    else:
        print("Error pulling changes from the remote repository:", result.stderr)


def get_date_7_days_ago():
    """Calculate the date for 7 days ago."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    return seven_days_ago.strftime('%Y-%m-%d')

def list_changed_files_in_past_week(repo_path):
    """List names of files changed from 7 days ago to today."""
    date_7_days_ago = get_date_7_days_ago()
    command = [
        "git", "-C", repo_path, "log", "--name-only", "--since", date_7_days_ago, "--pretty=format:", "--", "docs"
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    changed_files = set(filter(None, result.stdout.strip().split('\n')))
    
    if changed_files:
        print(f"Files changed from 7 days ago ({date_7_days_ago}) to today:")
        for file_path in changed_files:
            print(file_path)
            update_local_file(repo_path, file_path)
    else:
        print("No files have been changed in the last 7 days.")
    return changed_files

def update_local_file(repo_path, file_path):
    """Update or add the file in the local directory based on the repository, maintaining the directory structure."""
    source_path = os.path.join(repo_path, file_path)
    relative_path = os.path.relpath(source_path, repo_path)
    destination_path = os.path.join(local_training_data_dir, relative_path)

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    
    action = "Updating" if os.path.exists(destination_path) else "Adding"
    shutil.copy2(source_path, destination_path)
    print(f"{action}: {destination_path}")

def delete_storage_directory():
    """Delete the storage directory and all its contents."""
    if os.path.exists(storage_dir_path):
        shutil.rmtree(storage_dir_path)
        print(f"Deleted the storage directory: {storage_dir_path}")
    else:
        print("Storage directory not found. No deletion necessary.")

def run_training_script():
    """Run the training script."""
    print(f"Running training script: {training_script_path}")
    try:
        subprocess.run(["python3", training_script_path], check=True)
        print("Training script completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Training script failed with error: {e}")

def restart_pm2_process(process_id="1"):
    """Restart a PM2 process."""
    print(f"Restarting PM2 process with ID: {process_id}")
    try:
        subprocess.run(["pm2", "restart", process_id], check=True)
        print("PM2 process restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart PM2 process with error: {e}")

def send_slack_message(webhook_url, message):
    """Send a message to a Slack channel."""
    headers = {'Content-Type': 'application/json'}
    data = {"text": message}
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 200:
        print("Message sent to Slack successfully.")
    else:
        print(f"Failed to send message to Slack. Status code: {response.status_code}")

if __name__ == "__main__":
    print("Starting the automated data fetching and processing script...")
    git_pull(repo_path)
    changed_files = list_changed_files_in_past_week(repo_path)
    delete_storage_directory()
    run_training_script()
    restart_pm2_process()
    print("Script execution completed.")

    # Slack notification
    webhook_url = ""  # Your Slack Webhook URL
    message = f"1. {len(changed_files)} files changed last week.\n2. Updated the Training-data folder.\n3. New storage folder generated!\n4. Server restarted."
    send_slack_message(webhook_url, message)
