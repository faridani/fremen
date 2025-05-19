"""Flask application entry point."""

from flask import Flask
from flask_cors import CORS

from config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
)
from database import db
from models import *  # Import models so SQLAlchemy registers them
from auth_routes import auth_bp
from node_routes import node_bp
from workflow_routes import workflow_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialize and create the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Enable CORS for all routes
    CORS(app, supports_credentials=True)

    # Register API blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(node_bp, url_prefix="/api")
    app.register_blueprint(workflow_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)

