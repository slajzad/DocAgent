# DocAgent – Tester Edition

A lightweight, offline-ready LLM assistant tailored for infrastructure documentation.

---

## 🚀 Features

* 🧠 Auto-loading agents from `agents/` folder
* 🔍 Keyword and 📄 Vector search (ChromaDB)
* 🖥️ Minimal dashboard (FastAPI + HTMX)
* 📦 CLI client with REPL mode
* ✅ Multi-format document support (`.txt`, `.pdf`, `.docx`, `.md`)
* 🌓 Dark/light mode toggle

---

## ⚙️ System Requirements

* **CPU**: 2+ cores minimum
* **Memory**: 8 GB RAM recommended
* **Storage**: 25 GB (depends on model size and documents)
* **OS**: Linux, macOS, or WSL2
* **Docker**: Required for isolated model/runtime

---

## 📦 Installation

```bash
git clone https://github.com/slajzad/DocAgent.git
cd DocAgent
cp .env.example .env

# Install Docker Compose (if not already installed)
sudo apt install docker-compose

# Allow Docker usage without sudo (optional)
sudo usermod -aG docker $USER

# Build and run the project
sudo docker-compose up --build
```

> 🛠️ After containers start, open a **new terminal** and run:

```bash
# Pull the Mistral model into the Ollama container
docker exec -it docagent_ollama_1  ollama pull mistral

# Confirm the container is running (optional)
docker ps
```

Then visit: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)

---

## 🧪 Usage

**CLI Task**:

```bash
python3 cli/manage.py --agent doc_agent --input "How do I configure a VM?"
```

**REPL Mode**:

```bash
python3 cli/repl.py
```

---

## 📁 Project Structure

```
├── agents/
│   └── doc_agent/
│       ├── config.yaml
│       ├── docs/*.txt
│       └── agent.py
├── cli/
│   └── manage.py
├── orchestrator/
│   ├── api.py
│   ├── loader.py
│   ├── router.py
├── utils/
│   ├── logger.py
│   ├── doc_parser.py
│   └── context_retriever.py
```

---

## 🧼 Reset Recent History

To clear interaction logs:

```bash
rm logs/agent_log.jsonl
```

---

## ⚖️ Licensing Notice

DocAgent is released under the **MIT License**. It integrates third-party tools like **Ollama** and **Mistral**, which are subject to their respective licenses.

Ollama is source-available and must be downloaded separately via Docker or their official site. This project does not distribute or modify Ollama binaries.

**For business inquiries or licensing questions, contact:** [simon.glasberg@live.se](mailto:simon.glasberg@live.se)
