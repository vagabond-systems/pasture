import requests

ENDPOINT = "http://0.0.0.0:23023"


def test_grow_fock():
    response = requests.post(f"{ENDPOINT}/grow_flock")
    assert response.status_code == 200
