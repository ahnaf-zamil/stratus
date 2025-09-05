"""
Entry point for the user-facing Flask API.
Initializes database, CORS, and registers route blueprints.
"""

import os
import dotenv

from flask import Flask
from flask_cors import CORS

from .routes.deployments import deploy_bp
from .routes.applications import apps_bp
from .lib.db import db, migrate

# These imports are used for model registration with Flask-Migrate
# even though they aren't referenced directly in this file.
from .models.application import UserApplication, Deployment

# Load environment variables from .env file
dotenv.load_dotenv()

app = Flask(__name__)

# TODO: Move config to a dedicated config.py module
db_uri = os.environ.get("DB_URI")
if not db_uri:
    raise RuntimeError("Missing DB_URI in environment configuration")

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

# Enable CORS for frontend communication
CORS(app, supports_credentials=True)

# Initialize database and migration tooling
db.init_app(app)
migrate.init_app(app)

# Register route blueprints
app.register_blueprint(deploy_bp)
app.register_blueprint(apps_bp)
