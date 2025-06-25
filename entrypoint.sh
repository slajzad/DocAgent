#!/bin/bash

echo "🔥 Warming up Ollama..."
curl -s http://localhost:11434/api/generate -d '{"model": "mistral", "prompt": "Hello", "stream": false}' > /dev/null
echo "✅ Warm-up complete."

# Then launch the FastAPI app
exec uvicorn orchestrator.api:app --host 0.0.0.0 --port 8000 --reload