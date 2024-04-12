import requests

URL = "http://127.0.0.1:5000"


def embark():
    response = requests.post(f"{URL}/embark")
    payload = response.json()
    port = payload.get("content").get("port")
    print(f"embarked on port: {port}")
    return port


def ip_check(port):
    proxy_settings = {
        "http": f"http://0.0.0.0:{port}",
        "https": f"http://0.0.0.0:{port}",
    }
    url = "https://api.ipify.org?format=json"
    unproxied_ip = requests.get(url, timeout=3).json()["ip"]
    proxied_ip = requests.get(url, proxies=proxy_settings, timeout=3).json()["ip"]
    assert proxied_ip != unproxied_ip
    print(f"proxy functional on port: {port}, original: {unproxied_ip}, proxied: {proxied_ip}")
