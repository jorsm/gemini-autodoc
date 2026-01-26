# API Documentation

## Logic

All functions now include input validation using `check_input` to ensure parameters are numeric.

- **add(a, b, tax=0)**: Adds two numbers and optional tax. Raises `TypeError` if inputs are not numbers.
- **subtract(a, b)**: Subtracts two numbers. Raises `TypeError` if inputs are not numbers.
- **multiply(a, b)**: Multiplies two numbers. Raises `TypeError` if inputs are not numbers.
- **divide(a, b)**: Divides two numbers. Raises `TypeError` if inputs are not numbers or `DivisionByZeroError` if dividing by zero.
- **power(a, b)**: Raises a to the power of b. Raises `TypeError` if inputs are not numbers.
- **root(a, b)**: Takes the root of a number. Raises `TypeError` if inputs are not numbers.
- **modulus(a, b)**: Returns the remainder of division. Raises `TypeError` if inputs are not numbers or `DivisionByZeroError` if the divisor `b` is zero.
- **check_input(a, b)**: Checks if the input is valid. Raises `TypeError` if `a` or `b` are not integers or floats.
- **DivisionByZeroError**: Custom exception for division by zero.