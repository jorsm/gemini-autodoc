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
    - `paths` (list | str, optional): A list of file paths or a single file path to check. Defaults to `[".env", ".autodoc/.env"]`.
- **Behavior:**
    - Checks paths in order and skips missing files.
    - **No Override**: Only sets the environment variable if it does not already exist in the system environment (respects shell/OS exports).
    - **Parsing**: 
        - Skips empty lines and comments (lines starting with `#`).
        - Splits on the first `=` found.
        - Automatically unwraps single (`'`) or double (`"`) quotes surrounding values.

---

### Git Handler

#### `GitHandler(repo_path=".")`
A wrapper class for interacting with the local Git repository using `GitPython`. [source](../autodoc/utils/git_handler.py)

- **Initialization**:
    - Attempts to open the repository at `repo_path`. If the path is not a valid Git repository, `self.repo` is set to `None`, and methods will fail gracefully.
- **Methods:**
    - `get_changed_files(base="HEAD~1", head="HEAD") -> List[str]`: Compares two commits and returns a list of file paths relative to the repo root.
        - Filters for change types: **A** (Added), **M** (Modified), and **R** (Renamed).
        - Returns an empty list if the base commit cannot be found (e.g., initial commit) or if an error occurs.
    - `get_commit_context(commit="HEAD") -> dict`: Returns a dictionary containing metadata for a specific commit.
        - Keys: `hash`, `message`, `author`, `author_email`, and `date` (ISO format).
    - `get_root_dir() -> str`: Returns the absolute path to the repository's working directory. Falls back to `os.getcwd()` if not in a Git repo.

---

### Logger

#### `setup_logger(name="autodoc")`
Initializes and returns a configured Python `Logger` instance with dual handlers. [source](../autodoc/utils/logger.py)

- **Parameters:**
    - `name` (str): The name of the logger instance. Defaults to `"autodoc"`.
- **Behavior:**
    - **Level**: Set to `logging.INFO`.
    - **Directory**: Automatically creates a `.autodoc/logs/` directory in the current working directory.
    - **File Handler**: Uses a `RotatingFileHandler` writing to `.autodoc/logs/autodoc.log`.
        - **Max Size**: 1MB per file.
        - **Backup Count**: Keeps the 3 most recent log files.
    - **Console Handler**: Outputs formatted logs to the standard output (StreamHandler).
    - **Singleton-ish**: If a logger with the given name already has handlers attached, it returns the existing logger to avoid duplicate log entries.

---

## Examples

### Loading Environment Variables
```python
from autodoc.utils.env_loader import load_env

# Load from default locations: .env and .autodoc/.env
load_env()

# Load from a specific custom path (string or list)
load_env("secrets/.env.production")
```

### Checking Git Changes
```python
from autodoc.utils.git_handler import GitHandler

git = GitHandler()

# Get changes between the last two commits
changes = git.get_changed_files(base="HEAD~1", head="HEAD")
for file_path in changes:
    print(f"Modified: {file_path}")

# Get metadata for the latest commit
context = git.get_commit_context("HEAD")
print(f"Commit Hash: {context.get('hash')}")
print(f"Author: {context.get('author')}")
```

### Using the Logger
```python
from autodoc.utils.logger import setup_logger

# Initialize the standard autodoc logger
logger = setup_logger()

logger.info("Starting documentation generation...")

try:
    # ... logic ...
    logger.info("Processing complete.")
except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
```