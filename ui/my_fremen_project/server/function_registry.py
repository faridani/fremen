"""Utilities for compiling user provided node functions."""

from types import FunctionType


def compile_node_type_code(code_string: str) -> FunctionType:
    """Compile code defining a `run` function and return the callable."""
    local_namespace: dict[str, object] = {}
    exec(code_string, {}, local_namespace)
    func = local_namespace.get("run")
    if func is None or not isinstance(func, FunctionType):
        raise ValueError("No 'run' function found in the provided code")
    return func
