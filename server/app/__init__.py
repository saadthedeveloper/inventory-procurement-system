from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

    CORS(app)
    JWTManager(app)

    # Routes will be registered here later
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
