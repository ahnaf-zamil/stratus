from flask import Flask
from .routes.deployments import deploy_bp

app = Flask(__name__)

app.register_blueprint(deploy_bp)

if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True)
