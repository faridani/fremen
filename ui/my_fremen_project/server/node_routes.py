"""
node_routes.py
Routes related to NodeTypes (creating new node types, listing them, etc.)
"""

from flask import Blueprint, request, jsonify, session
from database import db
from models import User, NodeType

node_bp = Blueprint("nodes", __name__)

@node_bp.route("/node_types", methods=["GET"])
def get_node_types():
    """
    Get the list of node types accessible to the current user:
    - All public node types
    - The user's private node types
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # All public node types
    public_node_types = NodeType.query.filter_by(is_public=True).all()
    # The user's private node types
    private_node_types = NodeType.query.filter_by(user_id=user_id, is_public=False).all()

    # Combine
    result = []
    for nt in public_node_types + private_node_types:
        result.append({
            "id": nt.id,
            "name": nt.name,
            "is_public": nt.is_public
        })

    return jsonify(result), 200

@node_bp.route("/node_types", methods=["POST"])
def create_node_type():
    """
    Create a new NodeType (function) for the current user.
    Body should contain: name, code, is_public
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    code = data.get("code")
    is_public = data.get("is_public", False)

    if not name or not code:
        return jsonify({"error": "Missing name or code"}), 400

    # Create new node type
    node_type = NodeType(user_id=user_id, name=name, code=code, is_public=is_public)
    db.session.add(node_type)
    db.session.commit()

    return jsonify({"message": "Node type created", "node_type_id": node_type.id}), 201
