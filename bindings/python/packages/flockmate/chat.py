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

    def chat(self, prompt, temperature=None, tools=None, file_uris=None, response_schema=None):
        payload = {
            "prompt": prompt
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if tools is not None:
            payload["tools"] = tools
        if file_uris is not None:
            payload["file_uris"] = file_uris
        if response_schema is not None:
            payload["response_schema"] = response_schema
        response = requests.post(f"http://{self.host}:{self.port}/chat", json=payload)
        if response.status_code == 200:
            return response.json()["result"]
        else:
            raise ChatException(f"(!) chat failed with status: {response.status_code}")


class ChatException(Exception):
    pass
