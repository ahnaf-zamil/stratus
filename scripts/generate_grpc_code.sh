#!/bin/sh

PROTO_DIR=proto

mkdir -p shared

# Python
python -m grpc_tools.protoc \
    -I $PROTO_DIR \
    --python_out=shared \
    --grpc_python_out=shared \
    $PROTO_DIR/*.proto

# Golang
protoc \
    --go_out=deploy-node-agent --go_opt=paths=source_relative \
    --go-grpc_out=deploy-node-agent --go-grpc_opt=paths=source_relative \
    $PROTO_DIR/deployment_node.proto