import subprocess
from datetime import datetime, timedelta

# Path to your local git repository
repo_path = "/home/sumith/Desktop/Workspace/Demo/"

def get_date_7_days_ago():
    """Calculate the date for 7 days ago."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    return seven_days_ago.strftime('%Y-%m-%d')

def list_changed_files_in_past_week(repo_path):
    """List names of files changed from 7 days ago to today."""
    date_7_days_ago = get_date_7_days_ago()
    # Constructing the git log command to get changes from 7 days ago
    command = [
        "git", "-C", repo_path, "log", "--name-only", "--since", date_7_days_ago, "--pretty=format:", "--", "example"
    ]
    # Execute the git log command
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:  # Successfully executed command
        if result.stdout:
            changed_files = set(result.stdout.strip().split('\n'))
            if changed_files:
                print(f"Files changed from 7 days ago ({date_7_days_ago}) to today:")
                for file in changed_files:
                    if file:  # Avoid printing empty lines
                        print(file)
            else:
                print(f"No changes detected from 7 days ago ({date_7_days_ago}) to today.")
        else:
            print(f"No changes detected from 7 days ago ({date_7_days_ago}) to today.")
    else:
        print("Error executing git command:", result.stderr)

if __name__ == "__main__":
    list_changed_files_in_past_week(repo_path)
