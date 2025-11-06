import requests
from settings import OLLAMA_HOST


def init_llm():
    try:
        response = requests.get(f"{OLLAMA_HOST}")
        if response.status_code == 200:
            print("LLM initialized")
            print(response.raw.read().decode("utf-8"))
        else:
            print("Failed to initialize LLM")
    except Exception as e:
        print(e)
