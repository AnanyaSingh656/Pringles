#Both Agent() and LLM() are  library-defined classes imported from external packages (eg: CrewAI)
#syntax: variable= className()

import os
import sys
import time
from dotenv import load_dotenv

# Ensure Python can resolve files correctly across directories
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crewai import Agent, Task, Crew, Process, LLM
from tools.repo_parser import map_sandbox_structure, read_file_contents
from tools.file_writer import write_sandbox_file

# Load environment keys safely
load_dotenv()

# Define the unified model engine targeting stable endpoints
groq_llm = LLM(
    model="gemini/gemini-2.5-flash",
    max_retries=5,
    request_timeout=60.0
)

def rate_limit_cooldown(task_output):
    """Forcibly adds a 14-second pause after an agent task to protect RPM thresholds."""
    print("\n⏳ Cooldown active: Pausing pipeline execution thread for 14s...")
    time.sleep(14)
    return task_output

def launch_pringles_pipeline():
    print("\n==============================================")
    print("      Welcome to the Pringles Pipeline        ")
    print("==============================================")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice not in ["1", "2"]:
        print("❌ Invalid choice. Exiting pipeline.")
        return

    # Read the full codebase files dynamically up-front
    local_workspace_map = map_sandbox_structure()
    
    # Target path adjustment matching our visual capture tool boundaries
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sandbox_dir = os.path.join(base_dir, "src", "sandbox")
    
    important_files = ["README.md", "index.html", "styles.css", "main.py", "app.py", "package.json"]
    found_contents = []
    
    if os.path.exists(sandbox_dir):
        available_files = os.listdir(sandbox_dir)
        scan_targets = [f for f in important_files if f in available_files][:3]
        
        for file_name in scan_targets:
            try:
                text = read_file_contents(file_name)
                found_contents.append(f"--- {file_name} Contents ---\n{text}\n")
            except Exception:
                pass
    
    file_contents_context = "\n".join(found_contents) if found_contents else "No core source files detected in the root sandbox directory."
    
    # Read Blueprint Templates
    blueprint_path = os.path.join(base_dir, "pr_blueprint.md")
    try:
        with open(blueprint_path, "r", encoding="utf-8") as f:
            pr_blueprint_text = f.read()
    except Exception:
        pr_blueprint_text = "Standard PR Description & Testing Sections required."

    print(f"\n⚡ Initializing specialized crew for Option {choice}...")

    # 1. Base Discovery Team
    researcher = Agent(
        role='Lead Repository Architect',
        goal='Analyze structural codebase maps and trace file pathways.',
        backstory="You are an expert at identifying design architectures and indexing workspace layouts.",
        verbose=True,
        llm=groq_llm
    )

    crew_agents = [researcher]
    crew_tasks = []

    task1 = Task(
        description=(
            f"Examine this workspace directory layout map:\n\n{local_workspace_map}\n\n"
            f"Provide a clear layout summary of the files present in the sandbox workspace."
        ),
        expected_output="A brief summary of the workspace repository layout.",
        agent=researcher,
        callback=rate_limit_cooldown
    )
    crew_tasks.append(task1)

    # 2. Dynamic Execution Branching
    if choice == "1":
        bug_fixer = Agent(
            role='Bug-Fix Specialist',
            goal='Deep dive into raw file contents to find runtime bugs, structural flaws, or security vulnerabilities and fix them.',
            backstory="You are an elite code refactorer. You look at code logic to fix bugs and overwrite files using your tools.",
            verbose=True,
            llm=groq_llm,
            tools=[write_sandbox_file]
        )
        
        task2 = Task(
            description=(
                f"Review the structural layout and deep dive into the code text below:\n\n{file_contents_context}\n\n"
                f"CRITICAL REQUIREMENT: You MUST use your 'Write Sandbox File' tool right now to modify a file. "
                f"Locate any unclosed tags, bad formatting elements, or semantic optimization bugs. Update the file directly using the tool."
            ),
            expected_output="A summary of the files you modified and what bugs you squashed inside them.",
            agent=bug_fixer,
            callback=rate_limit_cooldown
        )
        crew_agents.append(bug_fixer)
        crew_tasks.append(task2)

    elif choice == "2":
        feature_engineer = Agent(
            role='Feature Engineer',
            goal='Analyze source files dynamically and add creative, high-value visual layout features.',
            backstory="You are a brilliant UI/UX developer. You look at code layouts, invent a feature that matches its theme, and modify the files using your tools.",
            verbose=True,
            llm=groq_llm,
            tools=[write_sandbox_file]
        )
        
        task2 = Task(
            description=(
                f"Analyze the repository's file structure and source text:\n\n{file_contents_context}\n\n"
                f"CRITICAL REQUIREMENT: Do not just build a footer. Look at the webpage layout and creatively "
                f"inject a new modern feature (like a clean navigation bar, a hero header section, or a thematic information grid) "
                f"to upgrade the app's design. Execute the 'Write Sandbox File' tool to apply your code changes directly."
            ),
            expected_output="A summary of the custom feature you designed and wrote into the workspace files.",
            agent=feature_engineer,
            callback=rate_limit_cooldown
        )
        crew_agents.append(feature_engineer)
        crew_tasks.append(task2)

    # 3. Add the Auditor/Reviewer to track changes
    auditor = Agent(
        role='Senior Code Auditor',
        goal='Review code modifications and ensure elite software engineering standards.',
        backstory="You are an exacting systems architect who prioritizes clean presentation and reliability.",
        verbose=True,
        llm=groq_llm
    )
    
    task3 = Task(
        description="Review the changes just executed by the specialists and compile an engineering audit report summarizing what was updated.",
        expected_output="A polished markdown audit report summarizing the actionable improvements.",
        agent=auditor,
        callback=rate_limit_cooldown
    )
    crew_agents.append(auditor)
    crew_tasks.append(task3)

    # 4. PR Automation Specialist Agent
    pr_specialist = Agent(
        role='PR Automation Specialist',
        goal='Draft impeccable Pull Request forms that strictly follow specified organization templates.',
        backstory="You are a coordination expert. You read generated local diff logging outputs to build hyper-accurate contribution descriptions.",
        verbose=True,
        llm=groq_llm
    )
    
    diff_log_path = os.path.join(base_dir, "last_code_diff.log")
    try:
        with open(diff_log_path, "r", encoding="utf-8") as f:
            live_diff_log = f.read()
    except Exception:
        live_diff_log = "No specific line comparison log generated yet."

    task4 = Task(
        description=(
            f"Take the Auditor's analysis and map it cleanly into the requested blueprint template format.\n\n"
            f"Requested PR Blueprint Template Layout:\n{pr_blueprint_text}\n\n"
            f"CRITICAL EVIDENCE (Read this to know exactly what lines changed):\n{live_diff_log}\n\n"
            f"Ensure the checkmark match corresponds exactly to the user selection choice option ({choice}): "
            f"If choice is 1 check [x] Bug Fix. If choice is 2 check [x] New Feature."
        ),
        expected_output="A complete, copy-pasteable markdown text file formatted exactly like the PR blueprint.",
        agent=pr_specialist
    )
    crew_agents.append(pr_specialist)
    crew_tasks.append(task4)

    # 5. Initialize the Engine Sequence
    pringles_crew = Crew(
        agents=crew_agents,
        tasks=crew_tasks,
        process=Process.sequential,
        verbose=True
    )

    print(f"\n🚀 Launching Live Code Modification Pipeline...")
    result = pringles_crew.kickoff()
    print("\n✨ Final Output (Formed Pull Request Draft):")
    print(result)

if __name__ == "__main__":
    launch_pringles_pipeline()