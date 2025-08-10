from flask import Flask
from flask_cors import CORS
from .routes.deployments import deploy_bp
from .routes.applications import apps_bp

from .lib.db import db, migrate

from .models.application import UserApplication, Deployment

import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URI"]

CORS(app, supports_credentials=True)
db.init_app(app)
migrate.init_app(app)

app.register_blueprint(deploy_bp)
app.register_blueprint(apps_bp)
