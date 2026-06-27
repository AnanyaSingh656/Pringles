# 💻 Pringles: Autonomous Multi-Agent GitHub Contribution Pipeline

> **"Once you pop, the PRs don't stop."** An advanced, sandboxed AI core designed to autonomously clone open-source repositories, analyze architecture layers, design and inject verified feature upgrades, and generate production-ready Pull Request documentation.

---

## 🏗️ System Architecture & Workflow Map

Pringles decouples orchestration from execution by utilizing a hierarchical multi-agent framework powered by CrewAI alongside a clean, state-synchronized Streamlit dashboard frontend.

```text
                               ┌───────────────────────────┐
                               │   Streamlit Web Interface │
                               └─────────────┬─────────────┘
                                             │
                       (User inputs Repo URL & Triggers Run)
                                             ▼
                               ┌───────────────────────────┐
                               │   Local Git Manager OS    │
                               └─────────────┬─────────────┘
                                             │
                        (Clones to /src/sandbox & Branches)
                                             ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │                               CrewAI Orchestration Core                               │
 │                                                                                       │
 │  ┌─────────────────────────┐             ┌────────────────────────────────────────┐   │
 │  │ Lead Repo Architect     │             │ Feature Engineer / Bug Specialist      │   │
 │  │ ─────────────────────── │             │ ────────────────────────────────────── │   │
 │  │ Parses directory maps   │             │ Evaluates source text; invokes local   │   │
 │  │ & creates structural    ├────────────►│ file-writing tools to inject creative  │   │
 │  │ workspace models.       │             │ UI features & optimize source code.    │   │
 │  └─────────────────────────┘             └───────────────────┬────────────────────┘   │
 │                                                               │                       │
 │                                                               ▼                       │
 │  ┌──────────────────────────┐             ┌────────────────────────────────────────┐  │
 │  │ PR Automation Specialist │             │ Senior Code Auditor                    │  │
 │  │ ──────────────────────── │             │ ────────────────────────────────────── │  │
 │  │ Structures final report  │◄────────────┤ Conducts downstream logic checks       │  │
 │  │ markdown with dynamic    │             │ to ensure elite engineering            │  │
 │  │ checklist verifications. │             │ and architectural standards.           │  │
 │  └──────────────────────────┘             └────────────────────────────────────────┘  │
 └───────────────────────────────────────────┬───────────────────────────────────────────┘
                                             │
                              (Generates Code Custom Diff)
                                             ▼
                               ┌───────────────────────────┐
                               │  Playwright Engine Core   │
                               └─────────────┬─────────────┘
                                             │
                         (Captures side-by-side PNG proofs)
                                             ▼
                               ┌───────────────────────────┐
                               │ Complete PR & Visual UI   │
                               │      Canvas Loaded        │
                               └───────────────────────────┘

```
### 🤖 Core Autonomous Agents
* **Lead Repository Architect:** Handles deep directory tree structural parsing and builds contextual data layout models.
* **Feature Engineer / Bug Specialist:** Evaluates source text directly and targets file-writing operations using sandboxed system tools.
* **Senior Code Auditor:** Conducts downstream checks to ensure elite software engineering presentation and structural adherence.
* **PR Automation Specialist:** Translates code logs and changes into structurally perfect markdown contribution documentation.

---

## 🚀 Key Architectural Features
* **Isolated Sandbox Execution:** All repository operations take place within an ephemeral tracking environment (`src/sandbox`) to guarantee local device security.
* **Playwright Visual Verification Loops:** Automatically invokes headless browser runs before and after core code mutation steps to capture side-by-side state screenshots.
* **Dynamic IO Interception:** Temporarily hooks and redirects Python standard output streaming components straight into a custom-designed web terminal interface.
* **API Resiliency Safeguards:** Implements strict task-level callback cooldown pad windows to successfully bypass aggressive rate limits (RPM constraints) on public model tiers.

---

## 🛠️ Installation & Local Setup

### Prerequisites
* Python 3.10 - 3.12
* Node.js (for Playwright system integrations)

### Installation Sequence
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/Pringles.git](https://github.com/YOUR_GITHUB_USERNAME/Pringles.git)
   cd Pringles


## 🛠️ Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AnanyaSingh656/Pringles.git
   cd Pringles
   ```

2. **Initialize and Activate Virtual Environment:**
   ```bash
   python -m venv venv

   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install Core Dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the project root and add:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key_here
   ```

5. **Launch the Engine Workspace:**
   ```bash
   streamlit run app.py
   ```
   
