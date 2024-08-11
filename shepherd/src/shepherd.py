import json
import os
import re
import time

import docker
import psycopg2
from loguru import logger
from psycopg2.extras import RealDictCursor

VERSION_TAG = os.getenv("VERSION_TAG")
logger.info(f"using version tag from env var: {VERSION_TAG}")
MAX_FLOCK_SIZE = int(os.getenv("MAX_FLOCK_SIZE"))
logger.info(f"using max flock size from env var: {MAX_FLOCK_SIZE}")
FLOCKMATE_IMAGE = os.getenv("FLOCKMATE_IMAGE")
logger.info(f"using flockmate image from env var: {FLOCKMATE_IMAGE}")
CREDS_DIRECTORY = os.getenv("CREDS_DIRECTORY")
logger.info(f"using creds directory from env var: {CREDS_DIRECTORY}")
FLOCKMATE_ENVIRONMENT = json.loads(os.getenv("FLOCKMATE_ENVIRONMENT"))
logger.info(f"using flockmate environment from env var: {FLOCKMATE_ENVIRONMENT}")


class Ledger:
    def __init__(self, docker_client):
        logger.info("( ) initializing ledger")
        host = "0.0.0.0"
        port = "23044"
        user = "pasture"
        password = "selah"
        database = "ledger"
        self.ledger_container = docker_client.containers.run(
            image=f"postgres:16.2-bookworm",
            name=f"pasture-ledger",
            hostname="ledger",
            detach=True,
            remove=True,
            ports={f"5432/tcp": port},
            network="pasture",
            environment={"POSTGRES_USER": user, "POSTGRES_PASSWORD": password, "POSTGRES_DB": database}
        )
        while "database system is ready to accept connections" not in str(self.ledger_container.logs()):
            logger.info("waiting for ledger to boot...")
            time.sleep(0.2)
        time.sleep(2)
        logger.info("acquiring psycopg connection")
        self.connection = psycopg2.connect(host=host, port=port, dbname=database, user=user, password=password)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        logger.info("creating tables")
        query = """
        CREATE TABLE flockmate (
            flockmate_id SERIAL PRIMARY KEY,
            port VARCHAR(64),
            created_at TIMESTAMPTZ,
            running BOOL
        );
        """
        self.cursor.execute(query)
        self.connection.commit()
        logger.info("(*) initialized ledger")


class Liaison:
    def __init__(self, docker_client):
        logger.info("( ) initializing liaison")
        port = "23023"
        docker_client.containers.run(
            image=f"josiahdc/liaison:{VERSION_TAG}",
            name=f"pasture-liaison",
            ports={f"{port}/tcp": port},
            detach=True,
            remove=True,
            network=f"pasture",
            environment={"MAX_FLOCK_SIZE": MAX_FLOCK_SIZE}
        )
        logger.info("(*) initialized liaison")


class Shepherd:
    def __init__(self):
        logger.info("( ) initializing shepherd")
        self.docker_client = docker.from_env()
        self.clear_infrastructure()
        self.network = self.docker_client.networks.create(
            name=f"pasture",
            driver="bridge"
        )
        self.ledger = Ledger(self.docker_client)
        self.liaison = Liaison(self.docker_client)
        logger.info("(*) initialized shepherd")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_infrastructure()

    def clear_infrastructure(self):
        self.docker_client.containers.prune()
        running_containers = self.docker_client.containers.list()
        for container in running_containers:
            if "pasture" in container.name:
                if not container.name == "pasture-shepherd":
                    container.remove(force=True)

        self.docker_client.networks.prune()
        networks = self.docker_client.networks.list()
        for network in networks:
            if "pasture" in network.name:
                network.remove()

    def tend(self):
        self.rectify_ledger()
        self.create_requested_flockmates()
        self.cull_extra_flockmates()

    def rectify_ledger(self):
        # determine the current state of the ledger
        query = """
            SELECT flockmate.flockmate_id, flockmate.port
            FROM flockmate
            WHERE flockmate.running = TRUE
        """
        self.ledger.cursor.execute(query)
        flockmates_in_ledger = self.ledger.cursor.fetchall()
        current_ledger = {}
        for flockmate in flockmates_in_ledger:
            current_ledger[flockmate["port"]] = flockmate["flockmate_id"]

        # determine the current state of the flock,
        # remove undocumented flockmates from pasture
        current_flock = []
        try:
            running_containers = self.docker_client.containers.list()
        except Exception as error:
            logger.info(f"error response from docker daemon when listing flockmates, ignoring")
            return
        for container in running_containers:
            if port_match := re.match(r"^pasture-flockmate-(\d+)$", container.name):
                port = port_match.group(1)
                if port not in current_ledger:
                    logger.info(f"removing undocumented flockmate from pasture: {container.name}")
                    try:
                        container.remove(force=True)
                    except Exception as error:
                        logger.info(f"error response from docker daemon when removing: {container.name}, ignoring")
                else:
                    current_flock.append(port)

        # remove dead flockmates from ledger
        for port, flockmate_id in current_ledger.items():
            if port not in current_flock:
                logger.info(f"removing dead flockmate from ledger - id: {flockmate_id}, port: {port}")
                query = """
                    DELETE
                    FROM flockmate
                    WHERE flockmate_id = %(flockmate_id)s;
                """
                parameters = {
                    "flockmate_id": flockmate_id
                }
                self.ledger.cursor.execute(query, vars=parameters)
                self.ledger.connection.commit()

    def create_requested_flockmates(self):
        query = """
            SELECT flockmate.flockmate_id, flockmate.port, flockmate.running
            FROM flockmate
            WHERE flockmate.running = FALSE
        """
        self.ledger.cursor.execute(query)
        requested_flockmates = self.ledger.cursor.fetchall()
        for flockmate in requested_flockmates:
            port = flockmate["port"]
            flockmate_id = flockmate["flockmate_id"]
            logger.info(f"creating requested flockmate: {flockmate_id} on port: {port}")
            self.docker_client.containers.run(
                image=f"{FLOCKMATE_IMAGE}:{VERSION_TAG}",
                name=f"pasture-flockmate-{port}",
                ports={f"23000/tcp": port},
                detach=True,
                network=f"pasture",
                remove=True,
                volumes={CREDS_DIRECTORY: {"bind": "/creds", "mode": "ro"}},
                environment=FLOCKMATE_ENVIRONMENT)
            self.register_flockmate(flockmate_id)

    def register_flockmate(self, flockmate_id):
        query = """
            UPDATE flockmate
            SET running = TRUE
            WHERE flockmate_id = %(flockmate_id)s;
        """
        parameters = {
            "flockmate_id": flockmate_id
        }
        self.ledger.cursor.execute(query, vars=parameters)
        self.ledger.connection.commit()

    def cull_extra_flockmates(self):
        query = """
            SELECT flockmate.flockmate_id, flockmate.created_at
            FROM flockmate
            ORDER BY flockmate.created_at DESC
        """
        self.ledger.cursor.execute(query)
        existing_flockmates = self.ledger.cursor.fetchall()
        if len(existing_flockmates) > MAX_FLOCK_SIZE:
            flockmates_to_prune = existing_flockmates[MAX_FLOCK_SIZE:]
            for flockmate in flockmates_to_prune:
                flockmate_id = flockmate["flockmate_id"]
                query = """
                    DELETE
                    FROM flockmate
                    WHERE flockmate_id = %(flockmate_id)s;
                """
                parameters = {
                    "flockmate_id": flockmate_id
                }
                self.ledger.cursor.execute(query, vars=parameters)
                self.ledger.connection.commit()
