import logging
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

        node_id = get_least_burdened_node()

        def send_grpc_req(host: str):
            # Connect to the least burdened Deployment Node's agent
            channel = grpc.insecure_channel(host)
            stub = DeploymentNodeStub(channel)
            grpc_response = stub.DeployApp(
                deployment_node_pb2.DeployAppRequest(
                    deployment_id=request.deployment_id
                )
            )
            return grpc_response

        try:
            # Send deploy request
            grpc_response = send_grpc_req(get_nodes()[node_id]["host"])
        except grpc._channel._InactiveRpcError:
            # Thrown if the node is down or if we cannot connect to it

            # Remove the node and retry
            remove_node(node_id)

            node_id = get_least_burdened_node()
            grpc_response = send_grpc_req(get_nodes()[node_id]["host"])

        return ResponseStatus(
            error=grpc_response.accepted,
            message=(
                f"Deployment {request.deployment_id} created"
                if grpc_response.accepted
                else "Error!"
            ),
        )
