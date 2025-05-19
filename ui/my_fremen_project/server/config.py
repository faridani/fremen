"""Configuration settings for the Flask application."""

import os

# Random secret key used for session signing. Override in production.
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

# Location of the SQLite database used during development.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

# Disable SQLAlchemy's event system to avoid overhead
SQLALCHEMY_TRACK_MODIFICATIONS = False
