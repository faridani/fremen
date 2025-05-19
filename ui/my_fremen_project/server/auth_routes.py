"""Routes handling user authentication."""

from flask import Blueprint, request, jsonify, session
from passlib.hash import pbkdf2_sha256
from database import db
from models import User

# Blueprint that groups authentication related endpoints
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Create a new user account."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    password_hash = pbkdf2_sha256.hash(password)
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and start a session."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not pbkdf2_sha256.verify(password, user.password_hash):
        return jsonify({"error": "Invalid password"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Login successful", "user_id": user.id}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Clear the current user session."""
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200

