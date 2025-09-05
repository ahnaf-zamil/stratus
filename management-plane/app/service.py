"""
gRPC service implementation for handling deployment requests.
Routes requests to the least burdened deployment node.
"""

import logging
import traceback
import grpc

from shared.proto_py.deployment_node_pb2_grpc import DeploymentNodeStub
from shared.proto_py import deployment_node_pb2
from shared.proto_py.deployments_pb2 import CreateDeployRequest, ResponseStatus
from shared.proto_py import deployments_pb2_grpc

from .nodes import get_least_burdened_node, get_nodes
from .exceptions import NoDeploymentNode


class DeploymentService(deployments_pb2_grpc.DeploymentServiceServicer):
    def CreateDeployment(
        self, request: CreateDeployRequest, _: grpc.ServicerContext
    ) -> ResponseStatus:
        logging.info(f"Received deployment request: {request.deployment_id}")

        def _dispatch_deploy_request():
            # Select least burdened node and send deployment request
            node_id = get_least_burdened_node()
            if not node_id:
                raise NoDeploymentNode("No deployment node is available. Retry later.")

            channel = grpc.insecure_channel(get_nodes()[node_id]["host"])
            stub = DeploymentNodeStub(channel)
            return stub.DeployApp(
                deployment_node_pb2.DeployAppRequest(
                    deployment_id=request.deployment_id
                )
            )

        try:
            grpc_response = _dispatch_deploy_request()
        except (grpc._channel._InactiveRpcError, NoDeploymentNode) as e:
            logging.error("Deployment failed:")
            logging.error("".join(traceback.format_exception(e)))
            return ResponseStatus(error=True, message=str(e))

        if not grpc_response.accepted:
            logging.warning(f"Deployment rejected by node for {request.deployment_id}")

        return ResponseStatus(
            error=not grpc_response.accepted,
            message=(
                f"Deployment {request.deployment_id} scheduled"
                if grpc_response.accepted
                else "Deployment rejected by node"
            ),
        )
