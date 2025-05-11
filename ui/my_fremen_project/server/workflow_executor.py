"""
workflow_executor.py
Contains logic to topologically sort a workflow's nodes and execute them
in the correct sequence.
Also supports conditional branching and sub-workflows if needed.
"""

import networkx as nx
import json
from function_registry import compile_node_type_code
from models import WorkflowNode, WorkflowEdge, NodeType, Workflow, db

def execute_workflow(workflow):
    """
    1. Build a directed graph with networkx.
    2. Topologically sort the nodes.
    3. For each node, retrieve the Python function (node_type code), run it,
       pass in inputs from the edges that led to this node.
    4. If the node returns a labeled output, follow the correct edges, etc.
    5. Return the final outputs or intermediate results as desired.
    """
    G = nx.DiGraph()

    # Add nodes
    for node in workflow.nodes:
        G.add_node(node.id, node_obj=node)

    # Add edges with label
    for edge in workflow.edges:
        G.add_edge(edge.source_node_id, edge.target_node_id, label=edge.label)

    # We'll do a simple topological sort for demonstration
    # However, note that conditional branching can skip nodes
    # In a real scenario you'd do a BFS or DFS that only follows the chosen edges
    try:
        sorted_nodes = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible as e:
        raise Exception("Cyclic dependency detected in the workflow") from e

    # We'll store the output of each node in a dictionary
    node_outputs = {}

    for node_id in sorted_nodes:
        node_data = G.nodes[node_id]["node_obj"]
        if not node_data.node_type_id:
            # This might be a subworkflow reference or something else
            # For now, let's skip or handle subworkflow logic
            node_outputs[node_id] = None
            continue

        node_type = NodeType.query.get(node_data.node_type_id)
        # Compile code
        func = compile_node_type_code(node_type.code)

        # Gather inputs from predecessor edges
        inputs = []
        pred_nodes = G.predecessors(node_id)
        for pn in pred_nodes:
            edge_data = G.get_edge_data(pn, node_id)
            # If the predecessor node had multiple outputs with labels, we might match by label.
            # For demonstration, just store the entire predecessor's output for now.
            inputs.append(node_outputs.get(pn, None))

        # If node_data.config is JSON, parse it
        config = {}
        if node_data.config:
            try:
                config = json.loads(node_data.config)
            except:
                pass

        # Call the function
        # For demonstration, let's assume the function signature is run(inputs, config)
        # The user can define it as they see fit.
        result = func(inputs, config)
        node_outputs[node_id] = result

    # For demonstration, return all node_outputs
    return node_outputs
