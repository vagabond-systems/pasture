import requests

ENDPOINT = "http://127.0.0.1:23109"


def test_chat():
    response = requests.post(f"{ENDPOINT}/chat", json={
        "prompt": "My favorite movie is Return of the King",
        "temperature": 1.0,
        "selected_files": [],
        "tools": []
    })
    print(response.content)
    response = requests.post(f"{ENDPOINT}/chat", json={
        "prompt": "What movies do I like?",
        "temperature": 1.0,
        "selected_files": [],
        "tools": []
    })
    print(response.content)


def test_tools():
    response = requests.post(f"{ENDPOINT}/chat", json={
        "prompt": "What's the weather like in LA today?",
        "temperature": 1.0,
        "selected_files": [],
        "tools": ["google_search"]
    })
    print(response.content)


def test_file():
    response = requests.post(f"{ENDPOINT}/chat", json={
        "prompt": "Please provide a summary of this document",
        "temperature": 1.0,
        "selected_files": ["raspberry-pi-pico-c-sdk.pdf"],
        "tools": []
    })
    print(response.content)
    response = requests.post(f"{ENDPOINT}/chat", json={
        "prompt": "How does one go about establishing an SPI connection with a raspberry pi pico?",
        "temperature": 1.0,
        "selected_files": [],
        "tools": []
    })
    print(response.content)
