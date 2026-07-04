import os
import json
import urllib.request
import urllib.error
import urllib.parse
import base64
import hashlib
import sys
from dotenv import load_dotenv

# Load environment variables from the local .env file
load_dotenv()

token = os.getenv("SATYAM_GITHUB_TOKEN")
owner = "satyamj9027"
repo = "assign"
local_dir = "."  # Sync the current directory

if not token:
    print("Error: SATYAM_GITHUB_TOKEN not found in .env file.")
    sys.exit(1)

# Files and directories to exclude from syncing
exclude_names = {
    ".env",
    ".git",
    "__pycache__",
    ".ipynb_checkpoints",
    ".vscode",
    ".idea"
}

def should_exclude(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    for p in parts:
        if p in exclude_names or p.endswith(".pyc"):
            return True
    return False

def git_sha1(data_bytes):
    s = hashlib.sha1()
    header = f"blob {len(data_bytes)}\x00".encode('utf-8')
    s.update(header)
    s.update(data_bytes)
    return s.hexdigest()

def make_request(url, method, headers, data=None):
    req = urllib.request.Request(url, method=method, headers=headers)
    if data is not None:
        if isinstance(data, dict):
            req.data = json.dumps(data).encode('utf-8')
        else:
            req.data = data
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            err_json = json.loads(body)
            msg = err_json.get("message", body)
        except:
            msg = body
        print(f"Error {method} {url}: {e.code} - {msg}")
        raise e

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "Python-urllib"
}

try:
    print("Fetching repo info to get default branch...")
    _, repo_info = make_request(f"https://api.github.com/repos/{owner}/{repo}", "GET", headers)
    branch = repo_info["default_branch"]
    print(f"Default branch is: {branch}")

    print("Fetching remote tree...")
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=true"
    _, tree_info = make_request(url, "GET", headers)

    remote_files = {} # path -> sha
    for item in tree_info.get("tree", []):
        if item["type"] == "blob":
            remote_files[item["path"]] = item["sha"]

    print(f"Found {len(remote_files)} files in remote repository.")

    # Find local files to sync
    local_files = {} # path -> bytes
    for root, dirs, files in os.walk(local_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_names]
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, local_dir).replace("\\", "/")
            if should_exclude(rel_path):
                continue
            try:
                with open(full_path, 'rb') as f:
                    content = f.read()
                local_files[rel_path] = content
            except Exception as e:
                print(f"Failed to read local file {rel_path}: {e}")

    print(f"Found {len(local_files)} files locally to push.")

    # Compare and push
    pushed_count = 0
    for rel_path, content in local_files.items():
        local_sha = git_sha1(content)
        remote_sha = remote_files.get(rel_path)
        
        if remote_sha == local_sha:
            continue
            
        print(f"Pushing file: {rel_path}...")
        encoded_content = base64.b64encode(content).decode('utf-8')
        put_data = {
            "message": f"Sync and update {rel_path}",
            "content": encoded_content,
            "branch": branch
        }
        if remote_sha:
            put_data["sha"] = remote_sha
            
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{urllib.parse.quote(rel_path)}"
        make_request(url, "PUT", headers, put_data)
        pushed_count += 1

    # Delete files no longer present locally
    deleted_count = 0
    for rel_path, sha in remote_files.items():
        if should_exclude(rel_path):
            continue
        if rel_path not in local_files:
            print(f"Deleting remote file: {rel_path}...")
            del_data = {
                "message": f"Clean up {rel_path}",
                "sha": sha,
                "branch": branch
            }
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{urllib.parse.quote(rel_path)}"
            make_request(url, "DELETE", headers, del_data)
            deleted_count += 1

    print(f"\n[OK] Success! Pushed {pushed_count} files, deleted {deleted_count} files.")

except Exception as e:
    print(f"\n[ERROR] Sync failed: {e}")
