from flask import Blueprint

apps_bp = Blueprint("applications", import_name=__name__, url_prefix="/apps")
