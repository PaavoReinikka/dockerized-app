"""
This script launches two applications, `agent_app.py` and `chat_app.py`, as separate processes.
"""

import subprocess

# Launch agent_app.py
agent_proc = subprocess.Popen(["python", "agent_app.py"])

# Launch chat_app.py
chat_proc = subprocess.Popen(["python", "chat_app.py"])

file_proc = subprocess.Popen(["python", "file_app.py"])

try:
    chat_proc.wait()
    agent_proc.wait()
    file_proc.wait()
except KeyboardInterrupt:
    agent_proc.terminate()
    chat_proc.terminate()
    file_proc.terminate()
finally:
    print("Processes terminated.")
    agent_proc.kill()
    chat_proc.kill()
    file_proc.kill()
