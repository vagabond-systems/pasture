import json

import requests

ENDPOINT = "http://127.0.0.1:23100"


def submit_request(payload, pdf_file_names):
    files = [("payload", ("payload.json", json.dumps(payload), "application/json"))]
    for pdf_file_name in pdf_file_names:
        files.append(("pdf", (pdf_file_name, open(pdf_file_name, "rb"), "application/pdf")))
    response = requests.post(f"{ENDPOINT}/chat", files=files)
    content = response.json()
    return content["result"]


def test_chat():
    payload = {
        "prompt": "My favorite movie is Return of the King",
        "temperature": 1.0,
        "tools": []
    }
    result = submit_request(payload, [])
    print(f"-------\n{result}\n")
    payload = {
        "prompt": "Name one movie you know I like.",
        "temperature": 1.0,
        "tools": []
    }
    result = submit_request(payload, [])
    print(f"-------\n{result}\n")


def test_tools():
    payload = {
        "prompt": "What's the weather like in LA today?",
        "temperature": 1.0,
        "tools": ["google_search"]
    }
    result = submit_request(payload, [])
    print(f"-------\n{result}\n")


def test_pdf():
    payload = {
        "prompt": "Please provide a summary of this document",
        "temperature": 1.0,
        "tools": []
    }
    result = submit_request(payload, ["pico_sdk.pdf"])
    print(f"-------\n{result}\n")
    payload = {
        "prompt": "What is the document's copyright?",
        "temperature": 1.0,
        "tools": []
    }
    result = submit_request(payload, [])
    print(f"-------\n{result}\n")
