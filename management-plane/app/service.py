import grpc

from shared import deployments_pb2_grpc
from shared.deployments_pb2 import CreateDeployRequest, ResponseStatus


class DeploymentService(deployments_pb2_grpc.DeploymentServiceServicer):
    def CreateDeployment(self, request: CreateDeployRequest, context: grpc.ServicerContext) -> ResponseStatus:
        # TODO: Create deployment 
        #       1. Select Deployment Node
        #       2. Send task to Deployment Node to deploy

        return ResponseStatus(error=False, message=f"Deployment {request.deployment_id} created")
