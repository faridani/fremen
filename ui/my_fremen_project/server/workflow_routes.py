"""
workflow_routes.py
Handles creation, update, retrieval, and execution of workflows (DAGs).
"""

from flask import Blueprint, request, jsonify, session
from database import db
from models import User, Workflow, WorkflowNode, WorkflowEdge, NodeType
from workflow_executor import execute_workflow

workflow_bp = Blueprint("workflows", __name__)

@workflow_bp.route("/workflows", methods=["GET"])
def get_workflows():
    """
    Return a list of workflows the user can see:
    - All public workflows
    - The user's private workflows
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    public_wfs = Workflow.query.filter_by(is_public=True).all()
    private_wfs = Workflow.query.filter_by(user_id=user_id, is_public=False).all()

    result = []
    for wf in public_wfs + private_wfs:
        result.append({
            "id": wf.id,
            "name": wf.name,
            "is_public": wf.is_public
        })

    return jsonify(result), 200

@workflow_bp.route("/workflows", methods=["POST"])
def create_workflow():
    """
    Create a new workflow with an initial name and visibility.
    Request body: { name, is_public }
    """
    user_id = session.get("user_id", None)
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
def get_workflow_detail(workflow_id):
    """
    Get the details (nodes, edges) of a workflow if the user has access.
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    # Check ownership or public
    if (wf.user_id != user_id) and (not wf.is_public):
        return jsonify({"error": "Forbidden"}), 403

    nodes = []
    for node in wf.nodes:
        nodes.append({
            "id": node.id,
            "node_type_id": node.node_type_id,
            "position": {"x": node.x, "y": node.y},
            "size": {"width": node.width, "height": node.height},
            "config": node.config
        })

    edges = []
    for edge in wf.edges:
        edges.append({
            "id": edge.id,
            "source": edge.source_node_id,
            "target": edge.target_node_id,
            "label": edge.label
        })

    return jsonify({
        "id": wf.id,
        "name": wf.name,
        "is_public": wf.is_public,
        "nodes": nodes,
        "edges": edges
    }), 200

@workflow_bp.route("/workflows/<int:workflow_id>", methods=["PUT"])
def update_workflow(workflow_id):
    """
    Update the workflow's name, visibility, nodes, and edges.
    Expect the front-end to send { name, is_public, nodes[], edges[] } to save.
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    # Check ownership
    if wf.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    wf.name = data.get("name", wf.name)
    wf.is_public = data.get("is_public", wf.is_public)

    # Clear existing nodes/edges and recreate them
    WorkflowNode.query.filter_by(workflow_id=wf.id).delete()
    WorkflowEdge.query.filter_by(workflow_id=wf.id).delete()

    # Create new nodes
    nodes_data = data.get("nodes", [])
    for nd in nodes_data:
        # node_type_id might be null if it's a sub-workflow reference or something
        node = WorkflowNode(
            workflow_id=wf.id,
            node_type_id=nd.get("node_type_id"),
            x=nd["position"]["x"],
            y=nd["position"]["y"],
            width=nd["size"]["width"],
            height=nd["size"]["height"],
            config=nd.get("config", "")
        )
        db.session.add(node)
        db.session.flush()  # to get an ID

    db.session.commit()

    # We have to re-fetch the nodes we just created to properly map IDs
    # In a real app, you'd handle ID mapping carefully. For simplicity, we assume
    # that the front end doesn't need consistent IDs across updates.
    # For a demonstration, let's just store edges referencing the new node IDs if needed.

    # Create new edges
    edges_data = data.get("edges", [])
    for ed in edges_data:
        edge = WorkflowEdge(
            workflow_id=wf.id,
            source_node_id=ed["source"],
            target_node_id=ed["target"],
            label=ed.get("label", "")
        )
        db.session.add(edge)

    db.session.commit()

    return jsonify({"message": "Workflow updated"}), 200

@workflow_bp.route("/workflows/<int:workflow_id>/run", methods=["POST"])
def run_workflow(workflow_id):
    """
    Execute the workflow DAG in topological order using networkx, etc.
    The user must have access to the workflow (own it or it's public).
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    # Check ownership or public
    if (wf.user_id != user_id) and (not wf.is_public):
        return jsonify({"error": "Forbidden"}), 403

    # Execute
    try:
        execution_result = execute_workflow(wf)
        return jsonify({"status": "success", "result": execution_result}), 200
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500
