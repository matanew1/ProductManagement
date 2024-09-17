from flask import Flask

from app.models import firebase_config
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
