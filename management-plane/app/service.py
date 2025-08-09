import logging
import sys
import traceback
import grpc

from shared.deployment_node_pb2_grpc import DeploymentNodeStub
from shared import deployment_node_pb2
from shared.deployments_pb2 import CreateDeployRequest, ResponseStatus
from shared import deployments_pb2_grpc

from .nodes import get_least_burdened_node, get_nodes, remove_node


class DeploymentService(deployments_pb2_grpc.DeploymentServiceServicer):
    def CreateDeployment(
        self, request: CreateDeployRequest, context: grpc.ServicerContext
    ) -> ResponseStatus:
        logging.info(f"Received deployment request: {request.deployment_id}")

        def send_grpc_req():
            # Connect to the least burdened Deployment Node's agent
            node_id = get_least_burdened_node()
            channel = grpc.insecure_channel(get_nodes()[node_id]["host"])
            stub = DeploymentNodeStub(channel)
            grpc_response = stub.DeployApp(
                deployment_node_pb2.DeployAppRequest(
                    deployment_id=request.deployment_id
                )
            )
            return grpc_response

        try:
            # Send deploy request
            grpc_response = send_grpc_req()
        except grpc._channel._InactiveRpcError as e:
            logging.error("".join(traceback.format_exception(e)))
            return ResponseStatus(error=True, message=str(e))

        return ResponseStatus(
            error=grpc_response.accepted,
            message=(
                f"Deployment {request.deployment_id} created"
                if grpc_response.accepted
                else "Error!"
            ),
        )
