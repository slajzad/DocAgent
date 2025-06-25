import yaml
import os
import importlib.util
from utils.doc_parser import parse_file

def load_agent_modules():
    agents = {}
    base_path = "agents"

    for name in os.listdir(base_path):
        path = os.path.join(base_path, name, "agent.py")
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            agents[name] = mod.handle_task  # assumes consistent interface

    return agents

def load_agent_config(agent_name):
    path = f"agents/{agent_name}/config.yaml"
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_agent_docs(agent_name):
    import fitz  # PyMuPDF
    import docx

    config = load_agent_config(agent_name)
    path = config.get("doc_path", "")
    chunks = []

    if os.path.isdir(path):
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if file.endswith(".txt"):
                with open(full_path, "r", encoding="utf-8") as f:
                    chunks.extend([p.strip() for p in f.read().split("\n\n") if p.strip()])

            elif file.endswith(".md"):
                with open(full_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    clean = text.replace("#", "").replace("*", "")
                    chunks.extend([p.strip() for p in clean.split("\n\n") if p.strip()])

            elif file.endswith(".docx"):
                doc = docx.Document(full_path)
                text = "\n".join([p.text for p in doc.paragraphs])
                chunks.extend([p.strip() for p in text.split("\n\n") if p.strip()])

            elif file.endswith(".pdf"):
                with fitz.open(full_path) as pdf:
                    text = "\n".join(page.get_text() for page in pdf)
                    chunks.extend([p.strip() for p in text.split("\n\n") if p.strip()])

    elif os.path.isfile(path):  # fallback for old paths
        with open(path, "r", encoding="utf-8") as f:
            chunks = [p.strip() for p in f.read().split("\n\n") if p.strip()]

    return chunks