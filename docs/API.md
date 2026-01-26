# API Documentation

## Logic

All functions now include input validation using `check_input` to ensure parameters are numeric.

- **add(a, b, tax=0)**: Takes two numbers and an optional `tax` parameter, and returns their sum. Raises `TypeError` if inputs are not numbers.
- **subtract(a, b)**: Subtracts the second number from the first. Raises `TypeError` if inputs are not numbers.
- **multiply(a, b)**: Multiplies two numbers. Raises `TypeError` if inputs are not numbers.
- **divide(a, b)**: Divides the first number by the second. Raises `TypeError` if inputs are not numbers or `ValueError` if dividing by zero.
- **check_input(a, b)**: Utility function that raises `TypeError` if `a` or `b` are not integers or floats.
