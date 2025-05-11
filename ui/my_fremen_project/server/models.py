"""
models.py
Defines our database models using SQLAlchemy.
"""

from datetime import datetime
from database import db

# Association of Users, Workflows, and Node types, etc.

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Relationship - a user has many workflows
    workflows = db.relationship("Workflow", back_populates="owner")

    # Relationship - a user has many node types
    node_types = db.relationship("NodeType", back_populates="owner")

class NodeType(db.Model):
    """
    NodeType holds custom Python code, function name, etc.
    If is_public=False, only the owner can use it.
    """
    __tablename__ = "node_types"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False)      # The Python function code
    is_public = db.Column(db.Boolean, default=False)

    # Relationship back to user
    owner = db.relationship("User", back_populates="node_types")

class Workflow(db.Model):
    """
    Workflow represents a DAG. 
    If is_public=False, only the owner can see it.
    """
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_public = db.Column(db.Boolean, default=False)

    # Relationship back to user
    owner = db.relationship("User", back_populates="workflows")

    # A workflow has many nodes
    nodes = db.relationship("WorkflowNode", back_populates="workflow", cascade="all, delete-orphan")
    # A workflow has many edges
    edges = db.relationship("WorkflowEdge", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowNode(db.Model):
    """
    A node in a workflow. Each node references a NodeType for its behavior.
    config can store JSON of custom parameters.
    """
    __tablename__ = "workflow_nodes"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    node_type_id = db.Column(db.Integer, db.ForeignKey("node_types.id"), nullable=True)
    x = db.Column(db.Float, default=0.0)
    y = db.Column(db.Float, default=0.0)
    width = db.Column(db.Float, default=200.0)
    height = db.Column(db.Float, default=100.0)
    config = db.Column(db.Text, nullable=True)  # JSON or other text

    # Relationship
    workflow = db.relationship("Workflow", back_populates="nodes")

class WorkflowEdge(db.Model):
    """
    An edge in a workflow. Possibly carry a label to support conditional logic.
    """
    __tablename__ = "workflow_edges"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    source_node_id = db.Column(db.Integer, db.ForeignKey("workflow_nodes.id"), nullable=False)
    target_node_id = db.Column(db.Integer, db.ForeignKey("workflow_nodes.id"), nullable=False)
    label = db.Column(db.String(50), nullable=True)

    # Relationship
    workflow = db.relationship("Workflow", back_populates="edges")
