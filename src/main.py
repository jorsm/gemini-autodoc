class DivisionByZeroError(Exception):
    """Custom exception for division by zero."""

    pass


def add(a, b, tax=0):
    """Adds two numbers and optional tax."""
    check_input(a, b)
    return a + b + tax


def subtract(a, b):
    """Subtracts two numbers."""
    check_input(a, b)
    return a - b


def multiply(a, b):
    """Multiplies two numbers."""
    check_input(a, b)
    return a * b


def divide(a, b):
    """Divides two numbers."""
    check_input(a, b)
    if b == 0:
        raise DivisionByZeroError("Cannot divide by zero.")
    return a / b


def power(a, b):
    """Raises a to the power of b."""
    check_input(a, b)
    return a**b


def check_input(a, b):
    """Checks if the input is valid."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numbers.")
