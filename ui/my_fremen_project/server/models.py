"""Database models used by the Flask application."""

from database import db


class User(db.Model):
    """Registered application user."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Relationships
    workflows = db.relationship("Workflow", back_populates="owner")
    node_types = db.relationship("NodeType", back_populates="owner")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class NodeType(db.Model):
    """Code snippet defining a user-provided node."""
    __tablename__ = "node_types"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Boolean, default=False)

    owner = db.relationship("User", back_populates="node_types")

    def __repr__(self) -> str:
        return f"<NodeType {self.name}>"


class Workflow(db.Model):
    """Collection of nodes and edges representing a DAG."""
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_public = db.Column(db.Boolean, default=False)

    owner = db.relationship("User", back_populates="workflows")
    nodes = db.relationship(
        "WorkflowNode",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )
    edges = db.relationship(
        "WorkflowEdge",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Workflow {self.name}>"


class WorkflowNode(db.Model):
    """Single step within a workflow."""
    __tablename__ = "workflow_nodes"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    node_type_id = db.Column(db.Integer, db.ForeignKey("node_types.id"), nullable=True)
    x = db.Column(db.Float, default=0.0)
    y = db.Column(db.Float, default=0.0)
    width = db.Column(db.Float, default=200.0)
    height = db.Column(db.Float, default=100.0)
    config = db.Column(db.Text, nullable=True)

    workflow = db.relationship("Workflow", back_populates="nodes")

    def __repr__(self) -> str:
        return f"<WorkflowNode {self.id}>"


class WorkflowEdge(db.Model):
    """Directed connection between workflow nodes."""
    __tablename__ = "workflow_edges"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    source_node_id = db.Column(
        db.Integer, db.ForeignKey("workflow_nodes.id"), nullable=False
    )
    target_node_id = db.Column(
        db.Integer, db.ForeignKey("workflow_nodes.id"), nullable=False
    )
    label = db.Column(db.String(50), nullable=True)

    workflow = db.relationship("Workflow", back_populates="edges")

    def __repr__(self) -> str:
        return f"<WorkflowEdge {self.source_node_id}->{self.target_node_id}>"

