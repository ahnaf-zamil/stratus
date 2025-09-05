"""
Routes for application-related API endpoints.
Includes runtime config retrieval and application creation.
"""

from http import HTTPStatus
from flask import Blueprint
from flask_pydantic import validate  # Validates request body against Pydantic schema

from ..lib.http import return_api_response, return_internal_error_response
from .schemas import CreateApplicationRequest
from ..models.application import UserApplication
from ..lib.db import db
from ..lib.runtimes import get_runtime_config

apps_bp = Blueprint("applications", import_name=__name__, url_prefix="/apps")


@apps_bp.get("/runtimes")
def get_runtimes():
    """Returns available runtimes from the YAML config."""
    return return_api_response(get_runtime_config(), HTTPStatus.OK)


@apps_bp.post("/create")
@validate()
def create_application(body: CreateApplicationRequest):
    """Creates a new user application in the database."""
    try:
        with db.session.begin():
            new_app = UserApplication(name=body.name, runtime=body.runtime)
            db.session.add(new_app)
    except Exception as e:
        # Log the error for debugging
        import logging

        logging.error(f"Error creating application: {e}")
        return return_internal_error_response("Error creating application")

    return return_api_response("Successfully created application", HTTPStatus.CREATED)
