"""Utility functions to execute workflows."""

from __future__ import annotations

import json
import networkx as nx

from function_registry import compile_node_type_code
from models import Workflow, WorkflowNode, WorkflowEdge, NodeType, db


def execute_workflow(workflow: Workflow) -> dict[int, object]:
    """Run all nodes in a workflow following topological order."""
    graph = nx.DiGraph()

    for node in workflow.nodes:
        graph.add_node(node.id, node_obj=node)
    for edge in workflow.edges:
        graph.add_edge(edge.source_node_id, edge.target_node_id, label=edge.label)

    try:
        sorted_nodes = list(nx.topological_sort(graph))
    except nx.NetworkXUnfeasible as exc:
        raise Exception("Cyclic dependency detected in the workflow") from exc

    node_outputs: dict[int, object] = {}

    for node_id in sorted_nodes:
        node_data: WorkflowNode = graph.nodes[node_id]["node_obj"]
        if not node_data.node_type_id:
            node_outputs[node_id] = None
            continue

        node_type = NodeType.query.get(node_data.node_type_id)
        func = compile_node_type_code(node_type.code)

        inputs = [node_outputs.get(pn) for pn in graph.predecessors(node_id)]

        config = {}
        if node_data.config:
            try:
                config = json.loads(node_data.config)
            except Exception:
                pass

        node_outputs[node_id] = func(inputs, config)

    return node_outputs

