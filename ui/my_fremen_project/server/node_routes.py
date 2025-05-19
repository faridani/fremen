"""API endpoints for managing custom node types."""

from flask import Blueprint, request, jsonify, session
from database import db
from models import NodeType

# Blueprint grouping node related endpoints
node_bp = Blueprint("nodes", __name__)


@node_bp.route("/node_types", methods=["GET"])
def get_node_types():
    """Return node types accessible to the current user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    public_node_types = NodeType.query.filter_by(is_public=True).all()
    private_node_types = NodeType.query.filter_by(
        user_id=user_id, is_public=False
    ).all()

    result = [
        {"id": nt.id, "name": nt.name, "is_public": nt.is_public}
        for nt in public_node_types + private_node_types
    ]
    return jsonify(result), 200


@node_bp.route("/node_types", methods=["POST"])
def create_node_type():
    """Create a new NodeType for the current user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    code = data.get("code")
    is_public = data.get("is_public", False)
    if not name or not code:
        return jsonify({"error": "Missing name or code"}), 400

    node_type = NodeType(user_id=user_id, name=name, code=code, is_public=is_public)
    db.session.add(node_type)
    db.session.commit()
    return jsonify({"message": "Node type created", "node_type_id": node_type.id}), 201

