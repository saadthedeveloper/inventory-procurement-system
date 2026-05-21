from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

    CORS(app)
    JWTManager(app)
    
    # Temporary test route
    @app.route('/')
    def home():
        return 'Server is running'
    
    @app.route('/test')
    def test():
        return jsonify({"status": "ok"})
    
    # Register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    
    # Debug: Print registered routes
    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} {list(rule.methods)}")
    print("========================\n")

    return app

