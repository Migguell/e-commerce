from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from config import Config
from database import db

def create_app(config_class=Config):
    """Application factory pattern for Flask app creation."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'ecommerce:'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    Session(app)
    
    # Initialize authentication middleware
    from auth.middleware import AuthMiddleware
    auth_middleware = AuthMiddleware(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.categories import categories_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'E-commerce API is running'}
    
    # Authentication status endpoint
    @app.route('/api/status')
    def api_status():
        from auth.middleware import AuthMiddleware
        return {
            'status': 'healthy',
            'message': 'E-commerce API is running',
            'authenticated': AuthMiddleware.is_authenticated(),
            'session_id': AuthMiddleware.get_session_id()
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)