import os
import re
import time
from time import sleep

import docker
import psycopg2
import requests
from loguru import logger
from psycopg2.extras import RealDictCursor

# set by user
VPN_USERNAME = os.getenv("VPN_USERNAME")
VPN_PASSWORD = os.getenv("VPN_PASSWORD")

# added by dockerfile during build
UNDERHILL_TAG = os.getenv("UNDERHILL_TAG")

IP_CHECK_MAX_ATTEMPTS = 5


class Trail:
    def __init__(self, docker_client, port):
        self.docker_client = docker_client
        self.port = port
        self.network = self.docker_client.networks.create(
            name=f"underhill-network-{self.port}",
            driver="bridge"
        )
        self.zenith = self.docker_client.containers.run(
            image=f"josiahdc/zenith:{UNDERHILL_TAG}",
            name=f"underhill-zenith-{self.port}",
            hostname="zenith",
            detach=True,
            privileged=True,
            network=f"underhill-network-{self.port}",
            dns=["1.1.1.1", "1.0.0.1"],
            environment={"VPN_USERNAME": VPN_USERNAME, "VPN_PASSWORD": VPN_PASSWORD}
        )
        self.switchback = self.docker_client.containers.run(
            image=f"josiahdc/switchback:{UNDERHILL_TAG}",
            name=f"underhill-switchback-{self.port}",
            detach=True,
            network_mode=f"container:underhill-zenith-{self.port}"
        )
        self.trailhead = self.docker_client.containers.run(
            image=f"josiahdc/trailhead:{UNDERHILL_TAG}",
            name=f"underhill-trailhead-{self.port}",
            hostname="trailhead",
            ports={f"{self.port}/tcp": self.port},
            detach=True,
            network=f"underhill-network-{self.port}",
            environment={"INGRESS_PORT": self.port}
        )

    def register(self, atlas):
        query = """
            INSERT INTO trail (port, demerits, created_at)
            VALUES (%(port)s, 0, now());
        """
        parameters = {
            "port": self.port
        }
        atlas.cursor.execute(query, vars=parameters)
        atlas.connection.commit()

    def is_operational(self):
        attempts = 0
        while attempts < IP_CHECK_MAX_ATTEMPTS:
            sleep(1)
            try:
                proxied_ip, unproxied_ip = self.ip_check()
                if proxied_ip != unproxied_ip:
                    logger.info("ip check passed", extra={"port": self.port,
                                                          "unproxied_ip": unproxied_ip,
                                                          "proxied_ip": proxied_ip})
                    return True
            except Exception as error:
                logger.warning("ip check failed", extra={"port": self.port, "error_str": str(error)})
        return False

    def ip_check(self):
        proxy_settings = {
            "http": f"http://0.0.0.0:{self.port}",
            "https": f"http://0.0.0.0:{self.port}",
        }
        url = "https://api.ipify.org?format=json"
        unproxied_ip = requests.get(url, timeout=3).json()["ip"]
        proxied_ip = requests.get(url, proxies=proxy_settings, timeout=3).json()["ip"]
        return unproxied_ip, proxied_ip

    def destroy(self):
        self.network.remove()
        self.trailhead.remove(force=True)
        self.switchback.remove(force=True)
        self.zenith.remove(force=True)
        logger.info("destroyed trail", extra={"port": self.port})


class Atlas:
    def __init__(self, docker_client):
        logger.info("( ) initializing atlas")
        host = "0.0.0.0"
        port = "5432"
        user = "underhill"
        password = "baggins"
        database = "atlas"
        self.container = docker_client.containers.run(
            image=f"postgres:16.2-bookworm",
            name=f"underhill-atlas",
            hostname="atlas",
            detach=True,
            ports={f"{port}/tcp": port},
            environment={"POSTGRES_USER": user, "POSTGRES_PASSWORD": password, "POSTGRES_DB": database},
            network="underhill-committee"
        )
        while "database system is ready to accept connections" not in str(self.container.logs()):
            logger.info("waiting for atlas to boot...")
            time.sleep(0.2)
        time.sleep(2)
        logger.info("acquiring psycopg connection")
        self.connection = psycopg2.connect(host=host, port=port, dbname=database, user=user, password=password)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        logger.info("creating tables")
        query = """
        CREATE TABLE trail (
            trail_id SERIAL PRIMARY KEY,
            port VARCHAR(64),
            demerits INT,
            created_at TIMESTAMPTZ
        );
        CREATE TABLE expedition (
            expedition_id SERIAL PRIMARY KEY,
            trail_id BIGINT REFERENCES trail(trail_id) NOT NULL
        );
        """
        self.cursor.execute(query)
        self.connection.commit()
        logger.info("(*) initialized atlas")


class Pathfinder:
    def __init__(self, docker_client):
        logger.info("( ) initializing pathfinder")
        self.container = docker_client.containers.run(
            image=f"josiahdc/pathfinder:{UNDERHILL_TAG}",
            name=f"underhill-pathfinder",
            hostname="pathfinder",
            detach=True,
            ports={"33033/tcp": "33033"},
            network="underhill-committee"
        )
        logger.info("(*) initialized pathfinder")


class Cartographer:
    def __init__(self, max_connections):
        logger.info("( ) initializing cartographer", extra={"max_connections": max_connections})
        self.available_ports = []
        for i in range(max_connections):
            port = str(33300 + i)
            self.available_ports.append(port)
        self.docker_client = docker.from_env()
        self.clear_infrastructure()
        self.network = self.docker_client.networks.create(
            name=f"underhill-committee",
            driver="bridge"
        )
        self.atlas = Atlas(self.docker_client)
        self.pathfinder = Pathfinder(self.docker_client)
        logger.info("(*) initialized cartographer", extra={"max_connections": max_connections})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_infrastructure()

    def clear_infrastructure(self):
        self.docker_client.containers.prune()
        running_containers = self.docker_client.containers.list()
        for container in running_containers:
            if "underhill" in container.name:
                if not container.name == "underhill-cartographer":
                    container.remove(force=True)

        self.docker_client.networks.prune()
        networks = self.docker_client.networks.list()
        for network in networks:
            if "underhill" in network.name:
                network.remove()

    def build_trail(self, port):
        logger.info("( ) creating trail", extra={"port": port})
        trail = Trail(self.docker_client, port)
        logger.info("testing trail", extra={"port": port})
        if trail.is_operational():
            trail.register(self.atlas)
            logger.info("(*) created trail", extra={"port": port})
            return trail
        else:
            logger.error("(!) trail creation failed", extra={"port": port})
            trail.destroy()
            return None

    def tend_trails(self):
        logger.info("tending trails")
        expected_ports = self.collect_expected_ports()
        established_ports = self.clear_unexpected_containers(expected_ports)

        # if a port is expected by the atlas, but not established in docker, create a trail
        for port in expected_ports:
            if port not in established_ports:
                self.build_trail(port)

        # add new trails on empty ports:
        for port in self.available_ports:
            if port not in expected_ports:
                self.build_trail(port)

        self.destroy_demerited_trails()

    def collect_expected_ports(self):
        query = """
            SELECT trail.port, trail.demerits, trail.created_at
            FROM trail
        """
        self.atlas.cursor.execute(query)
        charted_trails = self.atlas.cursor.fetchall()
        expected_ports = []
        for trail in charted_trails:
            expected_ports.append(trail["port"])
        deduplicated_result = list(set(expected_ports))
        return deduplicated_result

    def clear_unexpected_containers(self, expected_ports):
        established_ports = []
        running_containers = self.docker_client.containers.list()
        for container in running_containers:
            if port_match := re.match(r"^underhill-.*-(\d+)$", container.name):
                port = port_match.group(1)
                # if a container exists on an unexpected port, destroy it
                if port not in expected_ports:
                    container.remove(force=True)
                else:
                    established_ports.append(port)

        networks = self.docker_client.networks.list()
        for network in networks:
            if port_match := re.match(r"^underhill-.*-(\d+)$", network.name):
                port = port_match.group(1)
                if port not in expected_ports:
                    network.remove()
        deduplicated_result = list(set(established_ports))
        return deduplicated_result

    def destroy_demerited_trails(self):
        query = """
            SELECT trail.trail_id
            FROM trail
                 LEFT JOIN public.expedition on trail.trail_id = expedition.trail_id
            WHERE demerits > 0
            GROUP BY trail.trail_id
            HAVING count(expedition.expedition_id) < 1
        """
        self.atlas.cursor.execute(query)
        trail_data = self.atlas.cursor.fetchone()
        trail_id = trail_data["trail_id"]
        query = """
            DELETE FROM trail
            WHERE trail_id = %(trail_id)s
        """
        parameters = {
            "trail_id": trail_id
        }
        self.atlas.cursor.execute(query, vars=parameters)
        self.atlas.connection.commit()
