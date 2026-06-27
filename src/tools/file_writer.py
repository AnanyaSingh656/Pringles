#custom file-writing utility tool which allows the agents to modify local code

import os
import difflib
from crewai.tools import tool

@tool("Write Sandbox File")
def write_sandbox_file(file_name: str, content: str) -> str:
    """Useful to write or completely overwrite a specific file inside the src/sandbox directory with new code content."""
    base_path = "src/sandbox"
    file_path = os.path.join(base_path, file_name)
    
    if not os.path.exists(base_path):
        return f"Error: Sandbox directory '{base_path}' does not exist."
        
    try:
        # 1. Read old content if it exists to generate a Diff history comparison snapshot
        old_content = ""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                old_content = f.read()

        # 2. Overwrite file with new code content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 3. Compute structural changes and save them into a change log file
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            content.splitlines(keepends=True),
            fromfile=f"a/{file_name}",
            tofile=f"b/{file_name}"
        )
        diff_text = "".join(diff)

        # Write this diff log to our root folder for the PR agent to read later
        with open("last_code_diff.log", "w", encoding="utf-8") as f:
            f.write(diff_text if diff_text else f"No lines changed or file initialized for {file_name}.")

        return f"Success: Easily updated and wrote code contents directly to '{file_name}' inside the sandbox workspace!"
    except Exception as e:
        return f"Error writing to file '{file_name}': {str(e)}"