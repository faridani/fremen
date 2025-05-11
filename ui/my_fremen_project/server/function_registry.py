"""
function_registry.py
Stores and compiles user-defined functions from NodeType.
We can dynamically exec the code in a safe(ish) environment for demonstration.
In a real project, you'd want more security measures.
"""

import types

def compile_node_type_code(code_string):
    """
    Given a code string, compile it into a callable Python function object.
    We expect the code_string to define a function named 'run' or similar.
    This is extremely simplified for demonstration purposes.
    """
    # We'll use a dict as the local namespace for exec
    local_namespace = {}
    exec(code_string, {}, local_namespace)
    # We expect a function named 'run' in local_namespace
    func = local_namespace.get("run", None)
    if func is None or not isinstance(func, types.FunctionType):
        raise ValueError("No 'run' function found in the code")
    return func
