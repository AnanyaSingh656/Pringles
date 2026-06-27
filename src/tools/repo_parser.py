import os

def map_sandbox_structure(base_path="src/sandbox"):
    """Returns a visual string blueprint of the directory structure."""
    if not os.path.exists(base_path):
        return f"Directory '{base_path}' not found."
    
    blueprint = "### Cloned Sandbox Directory Blueprint:\n\n📁 sandbox/\n"
    for root, dirs, files in os.walk(base_path):
        for file in files:
            blueprint += f"      📄 {file}\n"
    return blueprint

def read_file_contents(file_name, base_path="src/sandbox"):
    """Safely reads and returns the raw text content inside a specific sandbox file."""
    file_path = os.path.join(base_path, file_name)
    
    if not os.path.exists(file_path):
        return f"Error: File '{file_name}' does not exist in the workspace sandbox."
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{file_name}': {str(e)}"