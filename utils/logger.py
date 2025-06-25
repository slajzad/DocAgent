import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("logs/agent_log.jsonl")  # Use Path object

def log_interaction(agent, input_text, response, duration_sec=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "input": input_text,
        "response": response,
    }

    if duration_sec is not None:
        entry["duration_sec"] = duration_sec

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")