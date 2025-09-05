"""
Node registry and health aggregation for the management plane.
Tracks active deployment nodes and selects the least burdened one.
"""

import json
import logging
import grpc

from shared.proto_py.deployment_node_pb2_grpc import DeploymentNodeStub
from google.protobuf import empty_pb2

_nodes = {}  # node_id -> {cpu, mem, host}


def get_nodes():
    return _nodes


def remove_node(node_id: str):
    _nodes.pop(node_id, None)


def healthcheck_node(host: str) -> str:
    """
    Performs a healthcheck RPC to the given node and updates its stats.
    Returns the node_id if successful.
    """
    channel = grpc.insecure_channel(host)
    stub = DeploymentNodeStub(channel)
    grpc_response = stub.HealthCheck(empty_pb2.Empty())

    _nodes[grpc_response.node_id] = {
        "cpu": grpc_response.cpu_perc,
        "mem": grpc_response.memory_perc,
        "host": host,
    }
    return grpc_response.node_id


def get_least_burdened_node():
    """
    Returns the node_id of the least burdened node based on CPU and memory.
    """
    if not _nodes:
        return None

    sorted_nodes = sorted(
        _nodes.items(), key=lambda item: (item[1]["cpu"], item[1]["mem"])
    )
    return sorted_nodes[0][0]


def check_deployment_nodes():
    """
    Loads node config and registers reachable nodes via healthcheck.
    """
    try:
        with open("../config.json", "r") as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config.json: {e}")
        return

    nodes_config = config.get("DEPLOYMENT_NODES", [])
    if not nodes_config:
        logging.warning("No deployment nodes found in config.")
        return

    for node in nodes_config:
        host = f"{node['ip']}:{node['port']}"
        try:
            node_id = healthcheck_node(host)
            logging.info(f"Registered node: {node_id} ({host})")
        except grpc.RpcError:
            logging.error(f"Node unreachable: {host}")

    logging.info(f"Total active nodes: {len(_nodes)}")
