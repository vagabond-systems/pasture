import requests
from user_agent import generate_user_agent


class Expedition:
    def __init__(self, underhill_host):
        self.underhill_host = underhill_host
        self.pathfinder_port = "33033"

        # connect to pathfinder
        response = requests.post(f"http://{self.underhill_host}:{self.pathfinder_port}/embark")
        content = response.json()
        self.port = content.get("port")
        self.expedition_id = content.get("expedition_id")

        # prepare session object
        self.session = requests.Session()
        self.session.headers.update({"user-agent": generate_user_agent(
            os=["win", "mac", "linux"],
            navigator=["chrome", "firefox"],
            device_type=["desktop"]
        )})
        self.proxy_settings = {
            "http": f"http://{underhill_host}:{self.port}",
            "https": f"http://{underhill_host}:{self.port}"
        }
        self.session.proxies.update(self.proxy_settings)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        payload = {"expedition_id": self.expedition_id}
        requests.post(f"http://{self.underhill_host}:{self.pathfinder_port}/conclude", json=payload)
        self.session.close()

    def demerit(self):
        payload = {"expedition_id": self.expedition_id}
        requests.post(f"http://{self.underhill_host}:{self.pathfinder_port}/demerit", json=payload)

    def head(self, *args, **kwargs):
        kwargs["proxies"] = self.proxy_settings
        return self.session.head(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs["proxies"] = self.proxy_settings
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs["proxies"] = self.proxy_settings
        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs["proxies"] = self.proxy_settings
        return self.session.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        kwargs["proxies"] = self.proxy_settings
        return self.session.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs["proxies"] = self.proxy_settings
        return self.session.delete(*args, **kwargs)
