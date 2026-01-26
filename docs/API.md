# API Documentation

## Logic

All functions now include input validation using `check_input` to ensure parameters are numeric.

- **add(a, b, tax=0)**: Takes two numbers and an optional `tax` parameter, and returns their sum. Raises `TypeError` if inputs are not numbers.
- **subtract(a, b)**: Subtracts the second number from the first. Raises `TypeError` if inputs are not numbers.
- **multiply(a, b)**: Multiplies two numbers. Raises `TypeError` if inputs are not numbers.
- **divide(a, b)**: Divides the first number by the second. Raises `TypeError` if inputs are not numbers or `DivisionByZeroError` if dividing by zero.
- **power(a, b)**: Raises `a` to the power of `b`. Raises `TypeError` if inputs are not numbers.
- **root(a, b)**: Takes the `b`-th root of `a`. Raises `TypeError` if inputs are not numbers.
- **check_input(a, b)**: Utility function that raises `TypeError` if `a` or `b` are not integers or floats.
- **DivisionByZeroError**: Custom exception raised when a division by zero is attempted.
