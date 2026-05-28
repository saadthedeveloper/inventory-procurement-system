from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
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
    from app.routes.products import products_bp
    from app.routes.categories import categories_bp
    from app.routes.units import units_bp
    from app.routes.suppliers import suppliers_bp
    from app.routes.purchase_orders import purchase_orders_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(purchase_orders_bp, url_prefix="/api/purchase-orders")	
    app.register_blueprint(units_bp, url_prefix="/api/units")
    app.register_blueprint(suppliers_bp, url_prefix="/api/suppliers")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")    
    # Debug: Print registered routes
    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} {list(rule.methods)}")
    print("========================\n")

    return app
