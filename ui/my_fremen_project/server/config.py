"""
config.py
Configuration settings for the Flask application.
"""

import os

# You can set SECRET_KEY to something random in production
SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

# SQLite database file (local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
