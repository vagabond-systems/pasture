import json
from time import sleep

import requests


def test_inference():
    print(f"\n")
    response = requests.post(f"http://localhost:23023/grow_flock")
    flockmate_port = response.json()["port"]
    print(f"flockmate port: {flockmate_port}")

    print(f"performing inference")
    request_data = [("payload", ("payload.json", json.dumps({
        "prompt": "Hi there!",
        "temperature": 1.0,
        "tools": []
    }), "application/json"))]
    response = requests.post(f"http://localhost:{flockmate_port}/chat", files=request_data)
    result = response.json()["result"]
    print(f"inference complete: \n---\n{result}\n---\n")

    request_data = [("payload", ("payload.json", json.dumps({
        "prompt": "Come up with a story about a shepherd tending a flock "
                  "of happy large language models in green pastures, near still waters?",
        "temperature": 2.0,
        "tools": []
    }), "application/json"))]
    response = requests.post(f"http://localhost:{flockmate_port}/chat", files=request_data)
    result = response.json()["result"]
    print(f"inference complete: \n---\n{result}\n---\n")

    request_data = [("payload", ("payload.json", json.dumps({
        "prompt": "Please continue your story",
        "temperature": 1.0,
        "selected_files": [],
        "tools": []
    }), "application/json"))]
    response = requests.post(f"http://localhost:{flockmate_port}/chat", files=request_data)
    result = response.json()["result"]
    print(f"inference complete: \n---\n{result}\n---\n")
