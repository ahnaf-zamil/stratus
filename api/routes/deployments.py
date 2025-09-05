"""
Routes for handling deployment creation.
Uploads user code, stores it in MinIO, and triggers deployment via gRPC.
"""

import os
import shutil
import zipfile
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, jsonify, render_template, request
from minio import Minio

from ..services.management_plane import ManagementPlaneService, deployments_pb2

deploy_bp = Blueprint("deployments", url_prefix="/deployments", import_name=__name__)

ZIP_FOLDER = "zips"
UPLOAD_FOLDER = "uploads"

# TODO: Move to config or environment variables
MINIO_HOST = "127.0.0.1:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "admin123"
DEPLOY_BUCKET = "stratus-deployments"

min_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


@deploy_bp.get("/create")
def create_deployment_page():
    """Serves the deployment creation HTML page."""
    return render_template("create_deployment.html")


@deploy_bp.post("/create")
def handle_deploy():
    """
    Handles deployment from user-provided code:
    1. Validates and saves uploaded files
    2. Zips the folder and uploads to MinIO
    3. Sends gRPC request to Management Plane
    """
    if "files" not in request.files:
        return "No files part", 400

    files = request.files.getlist("files")
    if not files or files[0].filename == "":
        return "No files selected", 400

    deployment_id = uuid4().hex

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(ZIP_FOLDER, exist_ok=True)

    upload_subfolder = os.path.join(UPLOAD_FOLDER, deployment_id)
    if os.path.exists(upload_subfolder):
        shutil.rmtree(upload_subfolder)
    os.makedirs(upload_subfolder, exist_ok=True)

    for file in files:
        raw_filename = file.filename
        parts = Path(raw_filename).parts
        parts_without_parent = parts[1:]  # remove top-level folder

        # Prevent directory traversal
        for part in parts_without_parent:
            if part in ("", ".", ".."):
                abort(400, f"Invalid path part: {part}")

        safe_rel_path = Path(*parts_without_parent)
        save_path = (Path(upload_subfolder) / safe_rel_path).resolve()

        if not str(save_path).startswith(str(Path(upload_subfolder).resolve())):
            abort(400, "Invalid path: potential directory traversal attempt")

        save_path.parent.mkdir(parents=True, exist_ok=True)
        file.save(str(save_path))

    # Zip the uploaded folder
    zip_path = os.path.join(ZIP_FOLDER, f"{deployment_id}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files_in_dir in os.walk(upload_subfolder):
            for fname in files_in_dir:
                file_path = os.path.join(root, fname)
                arcname = os.path.relpath(file_path, upload_subfolder)
                zipf.write(file_path, arcname)

    # Upload to MinIO
    bucket_exists = min_client.bucket_exists(DEPLOY_BUCKET)
    if not bucket_exists:
        min_client.make_bucket(DEPLOY_BUCKET)

    min_client.fput_object(
        DEPLOY_BUCKET,
        f"{deployment_id}.zip",
        zip_path,
    )

    # Cleanup local files
    shutil.rmtree(upload_subfolder)
    os.remove(zip_path)

    # Trigger deployment via gRPC
    stub = ManagementPlaneService.get_grpc_stub()
    grpc_response = stub.CreateDeployment(
        deployments_pb2.CreateDeployRequest(deployment_id=deployment_id)
    )

    return jsonify({"error": grpc_response.error, "message": grpc_response.message})
