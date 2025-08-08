import logging
import os
import threading
import grpc
from concurrent import futures
import time

from shared import deployments_pb2_grpc
from .service import DeploymentService
from .nodes import check_deployment_nodes
from .healthcheck import run_nodes_healthcheck

# Hardcoding right now
PORT = 50051
MAX_WORKERS = 5

logging.basicConfig(level=logging.DEBUG)


def serve_grpc_app():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    deployments_pb2_grpc.add_DeploymentServiceServicer_to_server(
        DeploymentService(), server
    )

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    logging.info(f"Stratus Management Plane running on port {PORT}")

    # cwd to source working dir
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    check_deployment_nodes()

    t1 = threading.Thread(target=run_nodes_healthcheck)
    try:
        t1.start()
    except KeyboardInterrupt:
        server.stop(0)
