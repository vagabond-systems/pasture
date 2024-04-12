import requests

from underhill.expedition import Expedition

ip_check_url = "https://api.ipify.org?format=json"


def test_expedition():
    overhill_ip = requests.get(ip_check_url).json()["ip"]
    with Expedition("0.0.0.0") as expedition:
        underhill_ip = expedition.get(ip_check_url).json()["ip"]
    assert overhill_ip != underhill_ip


def test_demerits():
    with Expedition("0.0.0.0") as expedition:
        expedition.demerit()

        # pause and confirm trail has been demerited, but is not removed
        pass
        with Expedition("0.0.0.0"):
            with Expedition("0.0.0.0"):
                with Expedition("0.0.0.0"):
                    # pause and confirm no new expedition has been assigned to trail
                    pass

    # pause and confirm trail has been rebuilt
    pass
