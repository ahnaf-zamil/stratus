"""
Service wrapper for communicating with the internal gRPC-based management plane.
Used by controllers to dispatch deployment-related requests.
"""

import grpc
from shared.proto_py import (
    deployments_pb2_grpc,
    deployments_pb2,
)  # This import is required for the route controllers

# TODO: Move to config or environment variable for flexibility
GRPC_ENDPOINT = "localhost:50051"


class ManagementPlaneService:
    @staticmethod
    def get_grpc_stub() -> deployments_pb2_grpc.DeploymentServiceStub:
        """
        Returns a gRPC stub for communicating with the DeploymentService.
        """
        channel = grpc.insecure_channel(GRPC_ENDPOINT)
        return deployments_pb2_grpc.DeploymentServiceStub(channel)
