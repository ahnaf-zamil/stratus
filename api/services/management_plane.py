from shared import deployments_pb2_grpc, deployments_pb2 # To be imported by controller
import grpc

GRPC_ENDPOINT = "localhost:50051"

class ManagementPlaneService:
    @staticmethod
    def get_grpc_stub() -> deployments_pb2_grpc.DeploymentServiceStub:
        channel = grpc.insecure_channel(GRPC_ENDPOINT)
        return deployments_pb2_grpc.DeploymentServiceStub(channel)