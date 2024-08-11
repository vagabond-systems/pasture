import requests

ENDPOINT = "http://127.0.0.1:23023"


def test_grow_herd():
    response = requests.post(f"{ENDPOINT}/grow_herd")
    assert response.status_code == 200
