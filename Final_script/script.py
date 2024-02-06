import subprocess
from datetime import datetime, timedelta
import shutil
import os

# Path to your local git repository
repo_path = "/home/sumith/Desktop/Workspace/push-website/"
# Path to the local directory where you want to store/update the files
local_training_data_dir = "/home/sumith/Desktop/Workspace/push-ai-chat/ai-python-code/Training-data"
# Path to the 'storage' directory that needs to be deleted
storage_dir_path = "/home/sumith/Desktop/Workspace/push-ai-chat/ai-python-code/storage"
# Path to the training script
training_script_path = "/home/sumith/Desktop/Workspace/push-ai-chat/ai-python-code/training.py"

def get_date_7_days_ago():
    """Calculate the date for 7 days ago."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    return seven_days_ago.strftime('%Y-%m-%d')

def list_changed_files_in_past_week(repo_path):
    """List names of files changed from 7 days ago to today and update local directory."""
    date_7_days_ago = get_date_7_days_ago()
    command = [
        "git", "-C", repo_path, "log", "--name-only", "--since", date_7_days_ago, "--pretty=format:", "--", "docs"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    changed_files = set(filter(None, result.stdout.strip().split('\n')))
    if changed_files:
        print(f"Files changed from 7 days ago ({date_7_days_ago}) to today:")
        for file_path in changed_files:
            print(file_path)
            update_local_file(repo_path, file_path, local_training_data_dir)
    else:
        print("No files have been changed in the last 7 days.")

def update_local_file(repo_path, file_path, local_dir):
    """Update or add the file in the local directory based on the repository."""
    source_path = os.path.join(repo_path, file_path)
    destination_path = os.path.join(local_dir, os.path.basename(file_path))
    
    action = "Updating" if os.path.exists(destination_path) else "Adding"
    shutil.copy2(source_path, destination_path)
    print(f"{action}: {destination_path}")

def delete_storage_directory(storage_dir_path):
    """Delete the storage directory and all its contents."""
    if os.path.exists(storage_dir_path):
        shutil.rmtree(storage_dir_path)
        print(f"Deleted the storage directory: {storage_dir_path}")
    else:
        print("Storage directory not found. No deletion necessary.")

def run_training_script(training_script_path):
    """Run the training script to possibly recreate the storage directory or perform training."""
    print(f"Running training script: {training_script_path}")
    try:
        subprocess.run(["python3", training_script_path], check=True)
        print("Training script completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Training script failed with error: {e}")

def restart_pm2_process(process_id):
    """Restart a PM2 process by its ID."""
    print(f"Restarting PM2 process with ID: {process_id}")
    try:
        subprocess.run(["pm2", "restart", process_id], check=True)
        print("PM2 process restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart PM2 process with error: {e}")

if __name__ == "__main__":
    print("Starting the automated data fetching and processing script...")
    list_changed_files_in_past_week(repo_path)
    delete_storage_directory(storage_dir_path)
    run_training_script(training_script_path)
    restart_pm2_process("1")
    print("Script execution completed.")
