#!/bin/sh

# The script works, DO NOT change it unless you know how to revert it in case you mess something up.

# Programming philosophy number 1: If it works, do NOT touch it.

PROTO_DIR=proto
OUT_DIR=shared

mkdir -p shared

# Python
python -m grpc_tools.protoc \
    -I $PROTO_DIR \
    --python_out=$OUT_DIR/proto_py \
    --grpc_python_out=$OUT_DIR/proto_py \
    $PROTO_DIR/*.proto

# Golang
protoc \
    --go_out=$OUT_DIR \
    --go-grpc_out=$OUT_DIR \
    $PROTO_DIR/*.proto