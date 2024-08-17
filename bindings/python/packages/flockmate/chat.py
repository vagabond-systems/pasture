import json
import mimetypes
import os

import requests


class PolygonChat:
    def __init__(self, host, port=None):
        # if port is none, start a new chat, otherwise continue chat on that port
        self.host = host
        if port is None:
            response = requests.post(f"http://{self.host}:23023/grow_flock")
            if response.status_code == 200:
                self.port = response.json()["port"]
            else:
                raise ChatException(f"(!) failed to start new chat with status: {response.status_code}")
        else:
            self.port = port

    def chat(self, prompt, temperature=1.0, tools=None, file_paths=None):
        if tools is None:
            tools = []
        if file_paths is None:
            file_paths = []
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "tools": tools
        }
        files = [("payload", ("payload.json", json.dumps(payload), "application/json"))]
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_path)[1]
            mimetype = mimetypes.types_map[file_extension]
            files.append(("file", (file_name, open(file_path, "rb"), mimetype)))
        response = requests.post(f"http://{self.host}:{self.port}/chat", files=files)
        if response.status_code == 200:
            return response.json()["result"]
        else:
            raise ChatException(f"(!) chat failed with status: {response.status_code}")


class ChatException(Exception):
    pass
