import json
import logging
import os

import grpc

from shared.deployment_node_pb2_grpc import DeploymentNodeStub
from shared.deployment_node_pb2 import HealthCheckResponse
from google.protobuf import empty_pb2

NODES = {}  # Node ID -> health status and host info


def get_nodes():
    return NODES


def remove_node(node_id: str):
    global NODES
    del NODES[node_id]


def healthcheck_node(host: str) -> str:
    # Get stats from node and add it to node dict
    global NODES
    channel = grpc.insecure_channel(host)
    stub = DeploymentNodeStub(channel)

    grpc_response = stub.HealthCheck(empty_pb2.Empty())

    NODES[grpc_response.node_id] = {
        "cpu": grpc_response.cpu_perc,
        "mem": grpc_response.memory_perc,
        "host": host,
    }
    return grpc_response.node_id


def get_least_burdened_node():
    nodes = get_nodes()
    sorted_nodes = sorted(
        nodes.items(), key=lambda item: (item[1]["cpu"], item[1]["mem"])
    )
    if len(sorted_nodes):
        least_burderened_node_id = sorted_nodes[0][0]
        return least_burderened_node_id
    else:
        return None


def check_deployment_nodes():
    with open("../config.json", "r") as f:
        config = json.load(f)

    for node in config["DEPLOYMENT_NODES"]:
        host = f"{node['ip']}:{node['port']}"
        try:
            node_id = healthcheck_node(host)
            logging.info(f"Registered node: {node_id} ({host})")
        except grpc.RpcError:
            logging.error(
                f"Deployment Node on {node['ip']}:{node['port']} cannot be reached."
            )

    logging.info(f"Total nodes: {len(NODES)}")
