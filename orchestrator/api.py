import os, json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from orchestrator.router import router, AGENT_CONFIGS
from orchestrator.loader import load_agent_docs
from utils.logger import log_interaction

app = FastAPI()
app.include_router(router)

templates = Jinja2Templates(directory="templates")

# --- Shared agent data enrichment ---
def get_agent_ui_data():
    agent_data = {}
    for agent_id, config in AGENT_CONFIGS.items():
        doc_count = 0
        doc_path = config.get("doc_path")

        if doc_path and os.path.isdir(doc_path):
            for file in os.listdir(doc_path):
                if file.endswith(".txt"):
                    with open(os.path.join(doc_path, file), "r") as f:
                        content = f.read()
                        doc_count += len([p for p in content.split("\n\n") if p.strip()])
        elif doc_path and os.path.isfile(doc_path):
            with open(doc_path, "r") as f:
                doc_count = len([p for p in f.read().split("\n\n") if p.strip()])

        agent_data[agent_id] = {
            **config,
            "docs_loaded": doc_count,
            "retrieval": "Vector" if config.get("use_vector") else "Keyword"
        }

    return agent_data

# --- GET Dashboard ---
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "agents": get_agent_ui_data()
    })

# --- POST Task submission ---
@app.post("/dashboard", response_class=HTMLResponse)
def submit_task(request: Request, agent: str = Form(...), input: str = Form(...)):
    from orchestrator.router import AGENTS
    result = AGENTS[agent](input)
    log_interaction(agent, input, result["response"])

    log_path = "logs/agent_log.jsonl"
    if os.path.isfile(log_path):
        with open(log_path) as f:
            history = [json.loads(line) for line in f.readlines()][-5:]
    else:
        history = []

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "agents": get_agent_ui_data(),
        "selected_agent": agent,
        "input_text": input,
        "response": result["response"],
        "duration": result.get("duration"),
        "model": result.get("model", AGENT_CONFIGS[agent].get("model", "n/a")),
        "load_time": result.get("load_time"),
        "inference_time": result.get("inference_time"),
        "history": reversed(history),
    })

# --- HTMX Log updates ---
@app.get("/logs", response_class=HTMLResponse)
def stream_logs(request: Request):
    log_path = "logs/agent_log.jsonl"
    if os.path.isfile(log_path):
        with open(log_path) as f:
            logs = [json.loads(line) for line in f.readlines()][-5:]
    else:
        logs = []

    return templates.TemplateResponse("partials/logs.html", {
        "request": request,
        "history": reversed(logs)
    })