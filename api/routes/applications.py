from flask import Blueprint, jsonify
from flask_pydantic import validate
from .schemas import CreateApplicationRequest

apps_bp = Blueprint("applications", import_name=__name__, url_prefix="/apps")


@apps_bp.get("/runtimes")
def get_runtimes():
    runtimes = [{"name": "Python", "version": "3.10", "id": "py310"}]
    return jsonify(runtimes)


@apps_bp.post("/create")
@validate()
def create_application(body: CreateApplicationRequest):

    print(body.name, body.runtime)

    return jsonify({})
