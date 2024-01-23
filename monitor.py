import requests
import time

def get_latest_commit_sha(owner, repo, token):
    headers = {
        'Authorization': f'Token {token}' if token else None,
    }

    # Get the latest commit SHA from the repository
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/commits', headers=headers)
    
    if response.status_code == 200:
        latest_commit_sha = response.json()[0]['sha']
        return latest_commit_sha
    else:
        print(f"Error: Unable to fetch latest commit. Status code: {response.status_code}")
        return None

def get_changed_files(owner, repo, base_commit, head_commit, token):
    headers = {
        'Authorization': f'Token {token}' if token else None,
    }

    # Compare two commits to get the list of changed files
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/compare/{base_commit}...{head_commit}', headers=headers)

    if response.status_code == 200:
        changed_files = [file['filename'] for file in response.json().get('files', [])]
        return changed_files
    else:
        print(f"Error: Unable to fetch changed files. Status code: {response.status_code}")
        return None

def monitor_repo_changes(owner, repo, token, interval_seconds=60):
    print(f"Monitoring changes in {owner}/{repo} every {interval_seconds} seconds...")

    # Initial commit SHA
    latest_commit_sha = get_latest_commit_sha(owner, repo, token)

    while True:
        # Get the latest commit SHA
        new_commit_sha = get_latest_commit_sha(owner, repo, token)

        # Check if there is a new commit
        if new_commit_sha and new_commit_sha != latest_commit_sha:
            print(f"New commit detected in {owner}/{repo}! SHA: {new_commit_sha}")
            
            # Get the added or modified files in the new commit
            changed_files = get_changed_files(owner, repo, latest_commit_sha, new_commit_sha, token)

            if changed_files:
                print("Changed files:")
                for file in changed_files:
                    print(f"- {file}")

            # Provide a direct link to the new commit
            commit_url = f"https://github.com/{owner}/{repo}/commit/{new_commit_sha}"
            print(f"Commit URL: {commit_url}")

            # Update latest commit SHA
            latest_commit_sha = new_commit_sha

        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Replace with GitHub username, repository name, and personal access token
    # E.G. - To monitor github.com/<owner>/<repo>
    owner = ""
    repo = ""
    github_token = ""

    monitor_repo_changes(owner, repo, github_token)
