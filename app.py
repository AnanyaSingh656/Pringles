import streamlit as st
import sys
import os
import contextlib
import builtins
import re
from io import StringIO

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.main import launch_pringles_pipeline

def clean_ansi_and_logs(text: str) -> str:
    """Filters string buffers to extract purely clean, raw execution logs."""
    text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m', '', text)
    text = re.sub(r'[─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬]|Task Started|Agent Final Answer', '', text)
    text = re.sub(r'.*CrewAIEventsBus.*', '', text)
    text = re.sub(r'!\[Before\].*|!\[After\].*|.*before\.png.*|.*after\.png.*', '', text)
    return text.strip()

# Initialize standard engine canvas setup
st.set_page_config(page_title="Pringles Workspace", layout="wide")

# Vercel / Linear Minimalist Interface Stylesheet Injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Core Framework Canvas Reset */
    .stApp {
        background-color: #09090B !important;
    }
    
    /* Destroy thick native Streamlit container borders globally */
    div[data-testid="stVerticalBlock"] > div, 
    div[data-testid="stCard"], 
    .stElementContainer {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }
    
    /* Strict Global Typography Scaling */
    h1, h2, h3, h4, p, span, label {
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #FAFAFA !important;
    }
    
    /* Input Labels and Layout Parameters */
    label p {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #A1A1AA !important;
        letter-spacing: 0.2px;
        margin-bottom: 6px !important;
    }
    
    /* Flat Surface Input Field Blocks (Cursor / Linear Style) */
    div[data-testid="stTextInput"] input {
        background-color: #18181B !important;
        color: #FAFAFA !important;
        border: 1px solid #27272A !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        transition: border-color 0.15s ease;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #E51A24 !important;
        box-shadow: none !important;
    }
    
    /* Premium Unified Action Call Button */
    div.stButton > button {
        background: #18181B !important;
        color: #FAFAFA !important;
        border: 1px solid #27272A !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.15s ease !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background: #27272A !important;
        border-color: #3F3F46 !important;
        color: #FAFAFA !important;
    }
    
    div.stButton > button:active {
        background: #E51A24 !important;
        border-color: #E51A24 !important;
        color: #ffffff !important;
    }
    
    /* High-End IDE VS Code Terminal Window Panel */
    .terminal-panel {
        background: #09090B !important;
        border-top: 1px solid #27272A;
        padding-top: 14px;
        height: 380px;
        overflow-y: auto;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #A1A1AA;
        line-height: 1.7;
        white-space: pre-wrap;
    }
    
    .terminal-line {
        color: #71717A;
        margin-right: 8px;
    }
    
    .terminal-success {
        color: #4ADE80;
    }
    
    /* Subtle Status Indicator Dot Pill */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 500;
        color: #A1A1AA;
        background: #18181B;
        padding: 4px 10px;
        border-radius: 9999px;
        border: 1px solid #27272A;
        margin-top: 10px;
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #71717A;
        border-radius: 50%;
    }
    
    .status-active .status-dot { background-color: #E51A24; box-shadow: 0 0 8px #E51A24; }
    .status-complete .status-dot { background-color: #4ADE80; }
    
    /* Image Section Frame Tweaks */
    img {
        border-radius: 8px;
        border: 1px solid #27272A;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App Minimal Header Section
st.markdown("<div style='margin-top: 15px; margin-bottom: 35px;'>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 26px; font-weight: 700; letter-spacing: -0.5px;'>Pringles</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 14px; color: #A1A1AA !important; margin-top: -5px;'>Autonomous GitHub Contribution Pipeline. <span style='color: #E51A24; font-weight: 500;'>Once you pop, the PRs don\'t stop.</span></p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Grid Matrix Parameters Layout
input_col1, input_col2, mode_col = st.columns([2, 1, 1])

with input_col1:
    target_repo_url = st.text_input("Repository URL", placeholder="https://github.com/owner/repo.git")

with input_col2:
    target_branch_name = st.text_input("Working Branch", placeholder="patch/analytics-fix")

with mode_col:
    mode_selection = st.selectbox("Pipeline Operation Mode", ("Fix an Existing Bug / Issue Analysis", "Add a Relevant New Feature"))

st.markdown("<div style='margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)
run_pipeline = st.button("Run Pipeline Engine")
st.markdown("</div>", unsafe_allow_html=True)

# Main Data Feed Workspace View Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<h3 style='font-size: 15px; font-weight: 600; letter-spacing: -0.1px; margin-bottom: 12px;'>Telemetry</h3>", unsafe_allow_html=True)
    log_container = st.empty()
    log_container.markdown('<div class="terminal-panel"><span class="terminal-line">></span> System engine idle. Awaiting initialization sequence...</div>', unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='font-size: 15px; font-weight: 600; letter-spacing: -0.1px; margin-bottom: 12px;'>Pull Request Draft</h3>", unsafe_allow_html=True)
    output_container = st.empty()
    output_container.markdown("<p style='font-size: 13px; color: #71717A !important;'>PR description blueprints will cleanly render here following automated verification tests.</p>", unsafe_allow_html=True)

# Unified Foot Section Image Rows
st.markdown("<div style='margin-top: 40px; margin-bottom: 20px; border-top: 1px solid #27272A; padding-top: 30px;'>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 15px; font-weight: 600;'>Visual Verification Proofs</h3>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.markdown("<p style='font-size: 13px; color: #A1A1AA !important;'>Before Execution State (before.png)</p>", unsafe_allow_html=True)
    before_viewer = st.empty()

with img_col2:
    st.markdown("<p style='font-size: 13px; color: #A1A1AA !important;'>After Execution State (after.png)</p>", unsafe_allow_html=True)
    after_viewer = st.empty()

# Operational Stream Pipeline Trigger Process Thread
if run_pipeline:
    if not target_repo_url or not target_branch_name:
        st.error("Error: All workspace inputs must be configured before pipeline launch.")
    else:
        choice_map = {"Fix an Existing Bug / Issue Analysis": "1", "Add a Relevant New Feature": "2"}
        active_choice = choice_map[mode_selection]
        
        class DynamicStreamCapture(StringIO):
            def write(self, s):
                super().write(s)
                raw_logs = self.getvalue()
                formatted_lines = []
                for line in raw_logs.splitlines():
                    cleaned_line = clean_ansi_and_logs(line)
                    if cleaned_line:
                        if "Success" in cleaned_line or "successfully" in cleaned_line:
                            formatted_lines.append(f'<span class="terminal-success">✓ {cleaned_line}</span>')
                        else:
                            formatted_lines.append(f'<span class="terminal-line">></span> {cleaned_line}')
                
                log_stream_html = "\n".join(formatted_lines)
                log_container.markdown(f'<div class="terminal-panel">{log_stream_html}</div>', unsafe_allow_html=True)
        
        capture_buffer = DynamicStreamCapture()
        
        status_box = st.markdown('<div class="status-badge status-active"><div class="status-dot"></div>Analyzing repository environment...</div>', unsafe_allow_html=True)
        
        old_input = builtins.input
        builtins.input = lambda prompt="": active_choice
        
        with contextlib.redirect_stdout(capture_buffer):
            try:
                from tools.git_manager import clone_target_repo, create_git_branch
                from tools.visual_capture import take_sandbox_screenshot
                
                print("Clearing target sandbox folder context arrays...")
                clone_target_repo(target_repo_url)
                take_sandbox_screenshot("before.png")
                create_git_branch(target_branch_name)
                
                launch_pringles_pipeline()
                take_sandbox_screenshot("after.png")
                
            except Exception as e:
                print(f"\nExecution Warning Aborted: {str(e)}")
                try:
                    take_sandbox_screenshot("after.png")
                except Exception:
                    pass
            finally:
                builtins.input = old_input
                    
        status_box.markdown('<div class="status-badge status-complete"><div class="status-dot"></div>Sequence Complete</div>', unsafe_allow_html=True)
        
        if os.path.exists("before.png"):
            before_viewer.image("before.png", use_container_width=True)
        if os.path.exists("after.png"):
            after_viewer.image("after.png", use_container_width=True)
            
        full_log = clean_ansi_and_logs(capture_buffer.getvalue())
        if "✨ Final Output (Formed Pull Request Draft):" in full_log or "Pull Request Contribution Report" in full_log:
            if "✨ Final Output (Formed Pull Request Draft):" in full_log:
                pr_draft = full_log.split("✨ Final Output (Formed Pull Request Draft):")[-1].strip()
            else:
                pr_draft = full_log.split("# 📝 Pull Request")[-1].strip()
                if pr_draft:
                    pr_draft = "# 📝 Pull Request" + pr_draft
                    
            pr_draft = re.sub(r'\|.*Before.*|\|.*:---.*|!\[Before\].*', '', pr_draft)
            output_container.markdown(pr_draft)
        else:
            output_container.error("Pipeline process track halted due to external rate boundaries. Review telemetry stream panels below.")