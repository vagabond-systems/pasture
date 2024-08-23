import logging
import os
from random import choice
from time import sleep

import psycopg2
import requests
from flask import Flask, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

if __name__ == "entrypoint":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    LEDGER_HOSTNAME = "ledger"
    LEDGER_PORT = "5432"
else:
    LEDGER_HOSTNAME = "127.0.0.1"
    LEDGER_PORT = "23044"
app.logger.setLevel(logging.INFO)

MAX_FLOCK_SIZE = int(os.getenv("MAX_FLOCK_SIZE"))
app.logger.info(f"using max flock size from env var: {MAX_FLOCK_SIZE}")
BASE_PORT = 23100
POTENTIAL_PORTS = [i + BASE_PORT for i in range(MAX_FLOCK_SIZE * 2)]
app.logger.info(f"app booted successfully, ready for requests!")


class Ledger:
    def __init__(self):
        self.connection = psycopg2.connect(host=LEDGER_HOSTNAME,
                                           port=LEDGER_PORT,
                                           dbname="ledger",
                                           user="pasture",
                                           password="selah")
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        app.logger.info("connected to ledger")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()


@app.route("/grow_flock", methods=["POST"])
def grow_flock():
    app.logger.info("received request to grow flock")
    payload = request.json
    system_instructions = payload.get("system_instructions", None)
    with Ledger() as ledger:
        port = create_flockmate(ledger)
        agent_initialization_payload = {
            "system_instructions": system_instructions
        }
        requests.post(f"http://pasture-flockmate-{port}:23000/initialize", json=agent_initialization_payload)
        return {"port": port}, 200


def create_flockmate(ledger):
    app.logger.info("( ) creating flockmate")
    query = """
        SELECT flockmate.port
        FROM flockmate
    """
    ledger.cursor.execute(query)
    flockmates = ledger.cursor.fetchall()
    used_ports = [int(flockmate["port"]) for flockmate in flockmates]
    available_ports = [port for port in POTENTIAL_PORTS if port not in used_ports]
    port = choice(available_ports)
    query = """
        INSERT INTO flockmate (port, created_at, running)
        VALUES (%(port)s, now(), false)
        RETURNING flockmate_id;
    """
    parameters = {
        "port": port
    }
    ledger.cursor.execute(query, vars=parameters)
    flockmate_id = ledger.cursor.fetchone()["flockmate_id"]
    ledger.connection.commit()
    app.logger.info("requested flockmate")

    running = False
    while not running:
        app.logger.info("awaiting flockmate creation...")
        sleep(0.3)
        query = """
            SELECT flockmate.running
            FROM flockmate
            WHERE flockmate_id = %(flockmate_id)s
        """
        parameters = {
            "flockmate_id": flockmate_id
        }
        ledger.cursor.execute(query, vars=parameters)
        flockmate = ledger.cursor.fetchone()
        running = flockmate["running"]
    app.logger.info("(*) created flockmate")
    return port
