"""
Outlook360 - One-Click Application Launcher
Launches the Streamlit Enterprise Dashboard on localhost.
"""
import sys
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    print("===================================================================")
    print("⚡ Starting Outlook360 - Universal Enterprise BI Platform          ")
    print("===================================================================")
    app_path = BASE_DIR / "app" / "main.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port=8501", "--server.headless=false"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[Outlook360] Server stopped by user.")
