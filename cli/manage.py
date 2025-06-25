import requests
import argparse
import json

API_URL = "http://localhost:8000/task"

def ask(prompt):
    return input(f"{prompt}: ").strip()

def send_task(agent, input_text, as_json=False):
    try:
        response = requests.post(API_URL, json={
            "agent": agent,
            "input": input_text
        })
        response.raise_for_status()
        result = response.json()

        print(f"\n✅ [Agent: {agent}]")
        if as_json:
            print(json.dumps(result, indent=2))
        else:
            print(result.get("response", "⚠️ No response field returned."))

    except requests.RequestException as e:
        print(f"\n❌ Request failed: {e}")
    except json.JSONDecodeError:
        print("\n❌ Could not parse JSON response.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a task to an AI agent")
    parser.add_argument("--agent", help="Agent name (e.g. doc_agent, other_agent)")
    parser.add_argument("--input", help="Prompt to send to the agent")
    parser.add_argument("--json", action="store_true", help="Show full JSON response")

    args = parser.parse_args()

    agent = args.agent or ask("Enter agent name")
    input_text = args.input or ask("Enter input prompt")

    send_task(agent, input_text, as_json=args.json)