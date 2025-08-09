from flask import Flask
from .routes.deployments import deploy_bp

from .lib.db import db, migrate

from .models.application import UserApplication, Deployment

import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_URI"]

db.init_app(app)
migrate.init_app(app)

app.register_blueprint(deploy_bp)