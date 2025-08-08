import grpc
from concurrent import futures
import time

from shared import deployments_pb2_grpc
from .service import DeploymentService

# Hardcoding right now
PORT = 50051
MAX_WORKERS = 10

def serve_grpc_app():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    deployments_pb2_grpc.add_DeploymentServiceServicer_to_server(
        DeploymentService(), server
    )

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    print(f"Stratus Management Plane running on port {PORT}")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)