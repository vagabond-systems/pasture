import subprocess
from time import sleep

import requests as requests
from flask import Flask
from loguru import logger

MAX_ATTEMPTS = 7


class Trail:
    def __init__(self):
        logger.info("( ) initializing trail")
        self.config_path = "/bough/openvpn/config"
        self.auth_path = "/bough/openvpn/auth"
        self.reflector_url = "https://api.ipify.org?format=json"
        self.overhill_address = self.collect_overhill_address()
        self.connect_openvpn()
        self.force_cloudflare_dns()
        self.start_proxy()
        self.confirm_connection()

        # prep flask
        self.flask_app = Flask("trail")
        self.flask_app.add_url_rule("/condemn", view_func=self.condemn, methods=["POST"])
        logger.info("(*) initialized trail")

    def condemn(self):
        logger.info("( ) shutting down")
        raise Exception("Shutdown!")

    def collect_overhill_address(self):
        logger.info(f"( ) collecting overhill address")
        overhill_address = requests.get(self.reflector_url).json()["ip"]
        logger.info(f"(*) collected overhill address: {overhill_address}")
        return overhill_address

    def connect_openvpn(self):
        logger.info("( ) starting openvpn")
        command = f"nohup openvpn --config {self.config_path} --auth-user-pass {self.auth_path} &"
        self.shell_exec(command)
        logger.info("(*) started openvpn")

    def force_cloudflare_dns(self):
        logger.info("( ) forcing cloudflare dns resolution")
        command = "echo 'nameserver 1.1.1.1\nnameserver 1.0.0.1\noptions edns0 trust-ad' > /etc/resolv.conf"
        self.shell_exec(command)
        logger.info("(*) forced cloudflare dns resolution")

    def start_proxy(self):
        logger.info("( ) starting proxy")
        command = "tinyproxy"
        # (~) if you want to debug, use `tinyproxy -d` instead
        self.shell_exec(command)
        logger.info("(*) started proxy")

    def confirm_connection(self):
        logger.info("( ) confirming disguise")
        proxy_settings = {
            "http": "http://0.0.0.0:33700",
            "https": "http://0.0.0.0:33700",
        }
        underhill_address = self.overhill_address
        current_attempts = 0
        while underhill_address == self.overhill_address and current_attempts < MAX_ATTEMPTS:
            current_attempts += 1
            try:
                logger.info(f"( ) collecting underhill address")
                sleep(0.5)
                underhill_address = requests.get(self.reflector_url, proxies=proxy_settings, timeout=3).json()["ip"]
                logger.info(f"(*) collected underhill address: {underhill_address}")
            except Exception as error:
                pass
        if current_attempts >= MAX_ATTEMPTS:
            raise Exception("Could not verify ipv4 address had changed (~) check vpn")
        logger.info(f"(*) confirmed disguise: {self.overhill_address} -> {underhill_address}")

    def shell_exec(self, command):
        subprocess.run(
            command,
            shell=True,
            encoding="UTF-8",
            check=True,
            capture_output=False
        )


def create_app():
    trail = Trail()
    return trail.flask_app


if __name__ == '__main__':
    trail = Trail()
    trail.flask_app.run(host="0.0.0.0", port=33700, threaded=False, processes=1)
