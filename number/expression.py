import numpy as np

def safe_eval(expr, variables):
    """
    Unsafe function to evaluate mathematical expressions.
    """
    try:
        return eval(expr, {"__builtins__": None}, variables)
    except Exception as e:
        raise ValueError(f"Could not evaluate expression: {expr}. Error: {str(e)}")