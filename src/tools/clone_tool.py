#creates custom built tools which we give to prebuilt agents given by CrewAI
#which we call as researcher and reviewer. The researcher uses the tool to download a repo and the reviewer audits the researcher's findings.

import os
import stat
import shutil
from git import Repo
from crewai.tools import tool

def remove_readonly(func, path, excinfo):
    """Helper to clear Windows read-only file locks on deletion failure."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

@tool("Download GitHub Repository")
def clone_repository(repo_url: str) -> str:
    """
    Clones a public GitHub repository into a local target sandbox folder for analysis.
    Input should be a valid GitHub HTTPS URL string.
    """
    target_dir = os.path.join(os.getcwd(), "src", "sandbox")
    
    # Clean up previous sandbox runs if they exist
    if os.path.exists(target_dir):
        try:
            shutil.rmtree(target_dir, onerror=remove_readonly)
        except Exception as e:
            return f"Error clearing old workspace folder: {str(e)}"
            
    # Attempt clean clone
    try:
        print(f"\n[Tool] Programmatically cloning {repo_url} into secure local sandbox...")
        Repo.clone_from(repo_url, target_dir)
        return f"Successfully cloned repository into local workspace at: {target_dir}. The workspace is ready for analysis."
    except Exception as e:
        return f"Failed to download repository. Error details: {str(e)}"