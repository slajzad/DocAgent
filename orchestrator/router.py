import os
import importlib.util
import yaml
import time
from fastapi import APIRouter, HTTPException
from orchestrator.models import TaskRequest
from utils.logger import log_interaction
from orchestrator.loader import load_agent_modules

router = APIRouter()

AGENT_DIR = "agents"
AGENTS = AGENTS = load_agent_modules()
AGENT_CONFIGS = {}

# --- Auto-discover agents and configs ---
for agent_name in os.listdir(AGENT_DIR):
    folder_path = os.path.join(AGENT_DIR, agent_name)
    agent_file = os.path.join(folder_path, "agent.py")
    config_file = os.path.join(folder_path, "config.yaml")

    if not os.path.isfile(agent_file):
        continue  # Skip if no agent.py

    # Load agent module
    spec = importlib.util.spec_from_file_location(f"{agent_name}_module", agent_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Register agent handler
    if hasattr(module, "handle_task"):
        AGENTS[agent_name] = module.handle_task
    else:
        print(f"[WARNING] No handle_task() found in {agent_name}")

    # Load config metadata
    if os.path.isfile(config_file):
        with open(config_file, "r") as f:
            AGENT_CONFIGS[agent_name] = yaml.safe_load(f)

        # Attach config to module so agent can access at import time
        setattr(module, "config", AGENT_CONFIGS[agent_name])

# --- Route: Submit a task ---
@router.post("/task")
def handle_task(request: TaskRequest):
    if request.agent in AGENTS:
        start = time.time()
        result = AGENTS[request.agent](request.input)
        duration = round(time.time() - start, 3)
        log_interaction(request.agent, request.input, result["response"], duration)
        return result
    raise HTTPException(status_code=404, detail="Agent not found")

# --- Route: List available agents ---
@router.get("/agent/{agent_name}")
def get_agent_metadata(agent_name: str):
    agent = AGENT_CONFIGS.get(agent_name)
    if agent:
        return agent
    raise HTTPException(status_code=404, detail="Agent not found")