from time import sleep

import requests as requests
from flask import Flask
from loguru import logger

MAX_ATTEMPTS = 7

app = Flask(__name__)


class Trail:
    def __init__(self):
        logger.info("( ) initializing trail")
        self.reflector_url = "https://api.ipify.org?format=json"
        self.overhill_address = self.collect_overhill_address()
        self.confirm_connection()
        logger.info("(*) initialized trail")

    def collect_overhill_address(self):
        logger.info(f"( ) collecting overhill address")
        overhill_address = requests.get(self.reflector_url).json()["ip"]
        logger.info(f"(*) collected overhill address: {overhill_address}")
        return overhill_address

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
