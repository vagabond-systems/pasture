from time import sleep

import requests


def test_inference():
    print(f"\n")
    response = requests.post(f"http://localhost:23023/grow_herd")
    flockmate_port = response.json()["port"]
    print(f"flockmate port: {flockmate_port}")
    print(f"waiting a moment for flockmate to boot...")
    sleep(3)
    print(f"performing inference")
    response = requests.post(f"http://localhost:{flockmate_port}/chat", json={
        "prompt": "Hi there!",
        "temperature": 1.0,
        "selected_files": [],
        "tools": []
    })
    result = response.json()["response"]
    print(f"inference complete: \n---\n{result}\n---\n")
    response = requests.post(f"http://localhost:{flockmate_port}/chat", json={
        "prompt": "Come up with a story about a shepherd tending a flock "
                  "of happy large language models in green pastures, near still waters?",
        "temperature": 2.0,
        "selected_files": [],
        "tools": []
    })
    result = response.json()["response"]
    print(f"inference complete: \n---\n{result}\n---\n")
    response = requests.post(f"http://localhost:{flockmate_port}/chat", json={
        "prompt": "Please continue your story",
        "temperature": 1.0,
        "selected_files": [],
        "tools": []
    })
    result = response.json()["response"]
    print(f"inference complete: \n---\n{result}\n---\n")
