# API Documentation

## Logic

All mathematical functions use the `sanitize_input` decorator to ensure parameters are numeric.

- **add_numbers(a, b)**: Adds two numbers.
  - **Parameters**:
    - `a` (int or float): The first number.
    - `b` (int or float): The second number.
  - **Returns**:
    - (int or float): The sum of `a` and `b`.
  - **Raises**:
    - `TypeError`: If `a` or `b` are not numbers (int or float).

- **subtract(a, b)**: Subtracts two numbers.
  - **Parameters**:
    - `a` (int or float): The first number.
    - `b` (int or float): The second number.
  - **Returns**:
    - (int or float): The result of `a` minus `b`.
  - **Raises**:
    - `TypeError`: If `a` or `b` are not numbers (int or float).

- **multiply(a, b)**: Multiplies two numbers.
  - **Parameters**:
    - `a` (int or float): The first number.
    - `b` (int or float): The second number.
  - **Returns**:
    - (int or float): The product of `a` and `b`.
  - **Raises**:
    - `TypeError`: If `a` or `b` are not numbers (int or float).

- **divide(a, b)**: Divides two numbers.
  - **Parameters**:
    - `a` (int or float): The numerator.
    - `b` (int or float): The denominator.
  - **Returns**:
    - (float): The result of `a` divided by `b`.
  - **Raises**:
    - `TypeError`: If `a` or `b` are not numbers (int or float).
    - `DivisionByZeroError`: If `b` is zero.

- **power(a, b)**: Raises `a` to the power of `b`.
  - **Parameters**:
    - `a` (int or float): The base.
    - `b` (int or float): The exponent.
  - **Returns**:
    - (int or float): The result of `a` raised to the power of `b`.
  - **Raises**:
    - `TypeError`: If `a` or `b` are not numbers (int or float).

- **modulus(a, b)**: Returns the remainder of division.
  - **Parameters**:
    - `a` (int or float): The dividend.
    - `b` (int or float): The divisor.
  - **Returns**:
    - (int or float): The remainder of `a` divided by `b`.
  - **Raises**:
    - `TypeError`: If `a` or `b` are not numbers (int or float).
    - `DivisionByZeroError`: If `b` is zero.

- **square(a)**: Returns the square of a number.
  - **Parameters**:
    - `a` (int or float): The number to square.
  - **Returns**:
    - (int or float): The result of `a` raised to the power of 2.
  - **Raises**:
    - `TypeError`: If `a` is not a number (int or float).

- **sanitize_input(func)**: Decorator that checks if the inputs are valid numbers.
  - **Parameters**:
    - `func` (callable): The function to be decorated.
  - **Returns**:
    - (callable): The wrapped function.
  - **Raises**:
    - `TypeError`: If the decorated function's arguments `a` or `b` are not integers or floats.

- **DivisionByZeroError**: Custom exception for division by zero.
  - **Inherits from**: `Exception`