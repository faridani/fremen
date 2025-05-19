"""Shared SQLAlchemy database instance."""

from flask_sqlalchemy import SQLAlchemy

# The database object is imported by modules that need database access.
db = SQLAlchemy()
