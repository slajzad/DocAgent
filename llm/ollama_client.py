import httpx
import os

def query_llm(prompt: str, model: str = "mistral") -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # Read fresh
    url = f"{base_url}/api/generate"
    print(f"[LLM] Sending request to: {url}")
    print(f"[LLM] Prompt: {prompt[:200]}...")  # Print only a snippet

    try:
        response = httpx.post(url, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=30)

        print("[LLM] Status code:", response.status_code)
        print("[LLM] Raw response:", response.text[:300])
        response.raise_for_status()

        return response.json().get("response", "")

    except Exception as e:
        print("[LLM] ERROR:", e)
        return "LLM call failed."