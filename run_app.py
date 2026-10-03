from pathlib import Path
import subprocess
import sys

app = Path(__file__).parent / "app" / "web_app.py"

subprocess.run([sys.executable, "-m", "streamlit", "run", str(app)], check=True)
