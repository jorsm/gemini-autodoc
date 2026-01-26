# Antigravity Calculator

A clean, robust Python library for basic mathematical operations with built-in validation and custom error handling.

## ✨ Features

- **Robust Operations**: Supports addition, subtraction, multiplication, and division.
- **Input Validation**: Automatically checks that inputs are numeric to prevent runtime errors.
- **Custom Exceptions**: Specialized `DivisionByZeroError` for clearer debugging.
- **Tax Support**: The `add` function includes an optional tax parameter for financial calculations.

## 🚀 Getting Started

### Prerequisites

- Python 3.6+

### Installation

Clone the repository and you're ready to go:

```bash
git clone https://github.com/yourusername/test-antigravity-agent.git
cd test-antigravity-agent
```

## 📖 Usage

Import the modules from `src/main.py` to start performing calculations:

```python
from src.main import add, divide

# Simple addition with tax
total = add(100, 20, tax=5)
print(f"Total: {total}") # Output: 125

# Safe division
try:
    result = divide(10, 0)
except Exception as e:
    print(e) # Output: Cannot divide by zero.
```

## 🛠️ Project Structure

- `src/main.py`: Core logic for all mathematical operations.
- `docs/API.md`: Detailed documentation for all functions and exceptions.
- `.agent/`: Internal agent configurations and workflows.

## � Development & Documentation

This project uses an automated Documentation Sync system. When you modify code in `src/`, a git hook will remind you to update the corresponding documentation.

To automatically sync documentation after making changes, you can ask the Antigravity agent:
> "Sync my docs"

## �📚 Documentation

For a full list of functions and their signatures, please refer to the [API Documentation](docs/API.md).

---

*Built with ❤️ by the Antigravity Team.*
