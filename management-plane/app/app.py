"""
Entry point for the Stratus Management Plane gRPC server.
Initializes the gRPC service, runs node discovery, and starts health checks.
"""

import logging
import os
import threading
import grpc
from concurrent import futures

from shared.proto_py import deployments_pb2_grpc
from .service import DeploymentService
from .nodes import check_deployment_nodes
from .healthcheck import run_nodes_healthcheck

# TODO: Move to config file or environment variables
PORT = 50051
MAX_WORKERS = 5

logging.basicConfig(level=logging.DEBUG)


def serve_grpc_app():
    # Ensure working directory is set to source root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Create and configure gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    deployments_pb2_grpc.add_DeploymentServiceServicer_to_server(
        DeploymentService(), server
    )
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    logging.info(f"Stratus Management Plane running on port {PORT}")

    # Discover and register deployment nodes
    check_deployment_nodes()

    # Start healthcheck thread
    healthcheck_thread = threading.Thread(target=run_nodes_healthcheck)
    try:
        healthcheck_thread.start()
        healthcheck_thread.join()
    except KeyboardInterrupt:
        logging.info("Shutting down gRPC server...")
        server.stop(0)
