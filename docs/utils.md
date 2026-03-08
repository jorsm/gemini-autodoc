# Utils

> **Overview**
> The `autodoc.utils` package provides essential helper modules for environment configuration, Git repository interaction, and standardized logging across the Auto-Doc system.

## Table of Contents
- [Utils](#utils)
  - [Table of Contents](#table-of-contents)
  - [Core Concepts](#core-concepts)
  - [API Reference](#api-reference)
    - [Environment Loader](#environment-loader)
      - [`load_env(paths=None)`](#load_envpathsnone)
    - [Git Handler](#git-handler)
      - [`GitHandler(repo_path=".")`](#githandlerrepo_path)
    - [Logger](#logger)
      - [`setup_logger(name="autodoc")`](#setup_loggernameautodoc)
  - [Examples](#examples)
    - [Loading Environment Variables](#loading-environment-variables)
    - [Checking Git Changes](#checking-git-changes)
    - [Using the Logger](#using-the-logger)

---

## Core Concepts

The utility layer is designed to be lightweight and focused:
- **Environment Management**: A custom `.env` loader that prioritizes system environment variables and supports multiple search paths without external dependencies.
- **Git Integration**: Encapsulates `GitPython` logic to identify changed files and extract commit metadata used for AI context generation.
- **Logging**: A pre-configured logging system that provides both real-time console feedback and persistent, rotating log files for troubleshooting.

---

## API Reference

### Environment Loader

#### `load_env(paths=None)`
Manually load environment variables from `.env` files into `os.environ`. [source](../autodoc/utils/env_loader.py)

- **Parameters:**
    - `paths` (list | str, optional): A list of file paths to check. Defaults to `[".env", ".autodoc/.env"]`.
- **Behavior:**
    - Checks paths in order.
    - Does not override existing environment variables (respects system/shell exports).
    - Handles comments (`#`) and strips quotes from values.

---

### Git Handler

#### `GitHandler(repo_path=".")`
A wrapper class for interacting with the local Git repository. [source](../autodoc/utils/git_handler.py)

- **Methods:**
    - `get_changed_files(base="HEAD~1", head="HEAD") -> List[str]`: Returns a list of file paths relative to the repo root that were Added (A), Modified (M), or Renamed (R) between two commits.
    - `get_commit_context(commit="HEAD") -> dict`: Returns a dictionary containing commit metadata: `hash`, `message`, `author`, `author_email`, and `date`.
    - `get_root_dir() -> str`: Returns the absolute path to the repository's working directory.

---

### Logger

#### `setup_logger(name="autodoc")`
Initializes and returns a configured Python `Logger` instance. [source](../autodoc/utils/logger.py)

- **Parameters:**
    - `name` (str): The name of the logger. Defaults to `"autodoc"`.
- **Behavior:**
    - Creates a `.autodoc/logs/` directory if it does not exist.
    - **File Handler**: Writes to `autodoc.log` with a 1MB rotation limit and 3-file backup history.
    - **Console Handler**: Outputs formatted logs to the standard output stream.

---

## Examples

### Loading Environment Variables
```python
from autodoc.utils.env_loader import load_env

# Load from default locations
load_env()

# Load from a specific custom path
load_env("config/.env.secret")
```

### Checking Git Changes
```python
from autodoc.utils.git_handler import GitHandler

git = GitHandler()
changes = git.get_changed_files(base="HEAD~1", head="HEAD")
print(f"Files modified in last commit: {changes}")

context = git.get_commit_context("HEAD")
print(f"Commit by {context['author']}: {context['message']}")
```

### Using the Logger
```python
from autodoc.utils.logger import setup_logger

logger = setup_logger("my_module")
logger.info("Starting documentation sync...")
try:
    # ... logic ...
    pass
except Exception as e:
    logger.error(f"Failed to process files: {e}")
```