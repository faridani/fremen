"""Endpoints for CRUD and execution of workflows."""

from flask import Blueprint, request, jsonify, session
from database import db
from models import Workflow, WorkflowNode, WorkflowEdge, NodeType
from workflow_executor import execute_workflow

workflow_bp = Blueprint("workflows", __name__)


@workflow_bp.route("/workflows", methods=["GET"])
def get_workflows():
    """Return all workflows visible to the current user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    public_wfs = Workflow.query.filter_by(is_public=True).all()
    private_wfs = Workflow.query.filter_by(user_id=user_id, is_public=False).all()
    result = [
        {"id": wf.id, "name": wf.name, "is_public": wf.is_public}
        for wf in public_wfs + private_wfs
    ]
    return jsonify(result), 200


@workflow_bp.route("/workflows", methods=["POST"])
def create_workflow():
    """Create a new workflow owned by the current user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    is_public = data.get("is_public", False)
    if not name:
        return jsonify({"error": "Missing workflow name"}), 400

    wf = Workflow(user_id=user_id, name=name, is_public=is_public)
    db.session.add(wf)
    db.session.commit()
    return jsonify({"message": "Workflow created", "workflow_id": wf.id}), 201


@workflow_bp.route("/workflows/<int:workflow_id>", methods=["GET"])
def get_workflow_detail(workflow_id: int):
    """Retrieve a workflow along with its nodes and edges."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    if (wf.user_id != user_id) and (not wf.is_public):
        return jsonify({"error": "Forbidden"}), 403

    nodes = [
        {
            "id": node.id,
            "node_type_id": node.node_type_id,
            "position": {"x": node.x, "y": node.y},
            "size": {"width": node.width, "height": node.height},
            "config": node.config,
        }
        for node in wf.nodes
    ]

    edges = [
        {
            "id": edge.id,
            "source": edge.source_node_id,
            "target": edge.target_node_id,
            "label": edge.label,
        }
        for edge in wf.edges
    ]

    return (
        jsonify({
            "id": wf.id,
            "name": wf.name,
            "is_public": wf.is_public,
            "nodes": nodes,
            "edges": edges,
        }),
        200,
    )


@workflow_bp.route("/workflows/<int:workflow_id>", methods=["PUT"])
def update_workflow(workflow_id: int):
    """Update a workflow definition."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404
    if wf.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    wf.name = data.get("name", wf.name)
    wf.is_public = data.get("is_public", wf.is_public)

    WorkflowNode.query.filter_by(workflow_id=wf.id).delete()
    WorkflowEdge.query.filter_by(workflow_id=wf.id).delete()

    nodes_data = data.get("nodes", [])
    for nd in nodes_data:
        node = WorkflowNode(
            workflow_id=wf.id,
            node_type_id=nd.get("node_type_id"),
            x=nd["position"]["x"],
            y=nd["position"]["y"],
            width=nd["size"]["width"],
            height=nd["size"]["height"],
            config=nd.get("config", ""),
        )
        db.session.add(node)
        db.session.flush()
    db.session.commit()

    edges_data = data.get("edges", [])
    for ed in edges_data:
        edge = WorkflowEdge(
            workflow_id=wf.id,
            source_node_id=ed["source"],
            target_node_id=ed["target"],
            label=ed.get("label", ""),
        )
        db.session.add(edge)
    db.session.commit()
    return jsonify({"message": "Workflow updated"}), 200


@workflow_bp.route("/workflows/<int:workflow_id>/run", methods=["POST"])
def run_workflow(workflow_id: int):
    """Execute the requested workflow."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    if (wf.user_id != user_id) and (not wf.is_public):
        return jsonify({"error": "Forbidden"}), 403

    try:
        result = execute_workflow(wf)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as exc:  # pragma: no cover - generic error propagation
        return jsonify({"status": "failure", "error": str(exc)}), 500

