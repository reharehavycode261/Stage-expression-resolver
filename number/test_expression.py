import pytest
from number.expression import safe_eval

def test_safe_eval_basic_expression():
    # Test basic arithmetic expression
    expr = "a + b"
    variables = {"a": 2, "b": 3}
    result = safe_eval(expr, variables)
    assert result == 5, "Basic addition failed"

def test_safe_eval_with_numpy():
    # Test expression with numpy function
    expr = "np.sqrt(a)"
    variables = {"a": 16, "np": np}
    result = safe_eval(expr, variables)
    assert result == 4, "Numpy sqrt failed"

def test_safe_eval_with_zero_division():
    # Test division by zero
    expr = "a / b"
    variables = {"a": 1, "b": 0}
    with pytest.raises(ValueError, match="Could not evaluate expression: a / b. Error: division by zero"):
        safe_eval(expr, variables)

def test_safe_eval_with_undefined_variable():
    # Test undefined variable
    expr = "a + b"
    variables = {"a": 1}
    with pytest.raises(ValueError, match="Could not evaluate expression: a + b. Error: name 'b' is not defined"):
        safe_eval(expr, variables)

def test_safe_eval_with_disallowed_builtins():
    # Test access to builtins should be disallowed
    expr = "__import__('os').system('echo hello')"
    variables = {}
    with pytest.raises(ValueError, match="Could not evaluate expression: __import__('os').system('echo hello'). Error: 'NoneType' object is not callable"):
        safe_eval(expr, variables)

def test_safe_eval_with_complex_expression():
    # Test complex expression
    expr = "(a + b) * (c - d)"
    variables = {"a": 2, "b": 3, "c": 5, "d": 1}
    result = safe_eval(expr, variables)
    assert result == 20, "Complex expression evaluation failed"

def test_safe_eval_with_empty_expression():
    # Test empty expression
    expr = ""
    variables = {}
    with pytest.raises(ValueError, match="Could not evaluate expression: . Error: unexpected EOF while parsing"):
        safe_eval(expr, variables)