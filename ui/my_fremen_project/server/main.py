"""
main.py
Entry point to run the Flask application.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask import g
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from models import *  # import all models so they are registered
from auth_routes import auth_bp
from node_routes import node_bp
from workflow_routes import workflow_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialize database
    db.init_app(app)

    # Enable CORS for all endpoints
    CORS(app, supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(node_bp, url_prefix="/api")
    app.register_blueprint(workflow_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
