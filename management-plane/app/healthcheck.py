"""Responsible for healthchecking and keeping track of deployment nodes"""

import json
import logging
import time

import grpc

from .nodes import get_nodes, healthcheck_node, remove_node

INTERVAL = 5  # Healthcheck interval in seconds


def run_nodes_healthcheck():
    logging.info(f"Running node healthchecks every {INTERVAL} seconds")

    # Load static node config from file
    with open("../config.json", "r") as f:
        config = json.load(f)

    while True:
        # Iterate over all nodes defined in config
        # This ensures nodes are re-added if they come back online
        for node in config["DEPLOYMENT_NODES"]:
            host = f"{node['ip']}:{node['port']}"
            try:
                node_id = healthcheck_node(host)
                logging.debug(f"Node alive: {node_id} ({host})")
            except grpc.RpcError:
                logging.error(f"Healthcheck failed for node: {host}")

                # Remove unreachable node from in-memory state
                nodes = get_nodes()
                for k in list(nodes.keys()):
                    if nodes[k]["host"] == host:
                        remove_node(k)

        time.sleep(INTERVAL)
