"""
Routes for application-related API endpoints.
Includes runtime config retrieval and application creation.
"""

from http import HTTPStatus
from typing import List, Optional
from flask import Blueprint
from flask_pydantic import validate  # Validates request body against Pydantic schema

from ..lib.http import return_api_response, return_internal_error_response
from .schemas import CreateApplicationRequest
from ..models.application import UserApplication
from ..lib.db import db
from ..lib.runtimes import get_runtime_config, get_runtime_by_id

apps_bp = Blueprint("applications", import_name=__name__, url_prefix="/apps")


@apps_bp.get("/runtimes")
def get_runtimes():
    """Returns available runtimes from the YAML config."""
    return return_api_response(get_runtime_config(), HTTPStatus.OK)


@apps_bp.get("/get/all")
def get_all_applications():
    """Returns a list of all applications"""
    apps: List[UserApplication] = (
        db.session.execute(db.select(UserApplication)).scalars().all()
    )
    return return_api_response([i.to_json() for i in apps], HTTPStatus.OK)


@apps_bp.get("/get/<app_id>")
def get_application_information(app_id):
    """Returns information about a user application in the database."""
    app: Optional[UserApplication] = db.session.execute(
        db.select(UserApplication).filter_by(id=app_id)
    ).scalar_one_or_none()
    if not app:
        return return_api_response({}, HTTPStatus.NOT_FOUND)

    return return_api_response(app.to_json(), HTTPStatus.OK)


@apps_bp.post("/create")
@validate()
def create_application(body: CreateApplicationRequest):
    """Creates a new user application in the database."""
    try:
        with db.session.begin():
            new_app = UserApplication(
                name=body.name, runtime=body.runtime, git_repo=str(body.git_repo)
            )
            db.session.add(new_app)
    except Exception as e:
        # Log the error for debugging
        import logging

        logging.error(f"Error creating application: {e}")
        return return_internal_error_response("Error creating application")

    return return_api_response("Successfully created application", HTTPStatus.CREATED)
