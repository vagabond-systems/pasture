import requests

from underhill.expedition import Expedition

ip_check_url = "https://api.ipify.org?format=json"


def test_expedition():
    overhill_ip = requests.get(ip_check_url).json()["ip"]
    with Expedition("0.0.0.0") as expedition:
        underhill_ip = expedition.get(ip_check_url).json()["ip"]
    assert overhill_ip != underhill_ip
