import json
import logging
import time

import grpc

from .nodes import get_nodes, healthcheck_node, remove_node

INTERVAL = 5  # seconds


def run_nodes_healthcheck():
    logging.info(f"Running node healthchecks every {INTERVAL} seconds")

    with open("../config.json", "r") as f:
        config = json.load(f)

    while True:
        # Going over all nodes in the config

        # Using the config instead of the node state dict ensures that in case a node comes back alive and its specified in the config, it will be added back to the state
        for node in config["DEPLOYMENT_NODES"]:
            host = f"{node['ip']}:{node['port']}"
            try:
                node_id = healthcheck_node(host)
                logging.debug(f"Node alive: {node_id} ({host})")
            except grpc.RpcError:
                logging.error(
                    f"Healthcheck failed for node: {node['ip']}:{node['port']}"
                )

                # If the node cannot be reached, then remove it from in-memory node list if it has been added before
                nodes = get_nodes()
                for k in list(nodes.keys()):
                    if nodes[k]["host"] == host:
                        remove_node(k)

        time.sleep(INTERVAL)
