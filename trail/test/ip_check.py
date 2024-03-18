import requests

proxy_settings = {
    "http": "http://0.0.0.0:3128",
    "https": "http://0.0.0.0:3128",
}
unproxied_response = requests.get("http://www.icanhazip.com")
proxied_response = requests.get("http://www.icanhazip.com", proxies=proxy_settings)

print(f"{unproxied_response.text.strip()} -> {proxied_response.text.strip()}")
