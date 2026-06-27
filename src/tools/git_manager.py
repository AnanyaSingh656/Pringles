#uses Python's built-in subprocess module to talk directly to your system's installed Git engine
#handles cleaning the sandbox
#cloning any repository URL you pass it, and branching automatically

import os
import shutil
import subprocess

def clean_sandbox(base_path="src/sandbox"):
    """Wipes out the sandbox directory completely, handling Windows permission blocks."""
    if os.path.exists(base_path):
        print(f"🧹 Clearing sandbox at {base_path}...")
        try:
            # Force read-only files to be writeable so they can be deleted cleanly
            for root, dirs, files in os.walk(base_path):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)
            shutil.rmtree(base_path, ignore_errors=True)
        except Exception:
            pass
    
    # Re-create fresh clean directory structure
    os.makedirs(base_path, exist_ok=True)
    return "Success: Sandbox cleaned."

def clone_target_repo(repo_url, base_path="src/sandbox"):
    """Clones any public GitHub repository URL directly into our sandbox folder."""
    # First, clean out whatever old project was sitting there
    clean_sandbox(base_path)
    
    print(f"📥 Cloning target repository: {repo_url}...")
    try:
        result = subprocess.run(
            ["git", "clone", repo_url, base_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return f"Success: Repository successfully cloned into {base_path}!"
    except subprocess.CalledProcessError as e:
        return f"Git Clone Failed: {e.stderr}"

def create_git_branch(branch_name, base_path="src/sandbox"):
    """Automatically switches to a brand-new isolated Git branch inside the repo."""
    if not os.path.exists(os.path.join(base_path, ".git")):
        return "Error: No active Git repository found in the sandbox."
        
    print(f"🌿 Creating isolated branch: {branch_name}...")
    try:
        # Run checkout -b inside the sandbox folder context
        result = subprocess.run(
            ["git", "-C", base_path, "checkout", "-b", branch_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return f"Success: Switched to branch '{branch_name}' natively."
    except subprocess.CalledProcessError as e:
        return f"Git Branching Failed: {e.stderr}"