import requests
import time

start = time.time()

response = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={
        "model": "qwen3:4b",
        "prompt": "What is AI?",
        "stream": False,
        "think": False
    },
    timeout=300
)

print(response.json()["response"])
print("Time:", time.time() - start)