from functools import wraps


class DivisionByZeroError(Exception):
    """Custom exception for division by zero."""

    pass


def sanitize_input(func):
    """Decorator that checks if the inputs are valid numbers."""

    @wraps(func)
    def wrapper(a, b):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numbers.")
        return func(a, b)

    return wrapper


@sanitize_input
def add(a, b):
    """Adds two numbers."""
    return a + b


@sanitize_input
def subtract(a, b):
    """Subtracts two numbers."""
    return a - b


@sanitize_input
def multiply(a, b):
    """Multiplies two numbers."""
    return a * b


@sanitize_input
def divide(a, b):
    """Divides two numbers."""
    if b == 0:
        raise DivisionByZeroError("Cannot divide by zero.")
    return a / b


@sanitize_input
def power(a, b):
    """Raises a to the power of b."""
    return a**b


@sanitize_input
def modulus(a, b):
    """Returns the remainder of division."""
    if b == 0:
        raise DivisionByZeroError("Cannot divide by zero.")
    return a % b


def square(a):
    """Returns the square of a number."""
    return power(a, 2)
