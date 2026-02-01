# Utilities

This page provides documentation for the utility modules used within the Auto-Doc system to handle version control operations and logging.

## Git Handler

The `autodoc.utils.git_handler` module provides a wrapper around `GitPython` to manage repository interactions and track file changes.

### `GitHandler` Class

Handles interactions with the local Git repository.

#### Methods

- **`__init__(repo_path: str = ".")`**
  Initializes the handler. If the provided path is not a valid Git repository, the internal repository reference is set to `None`.
  
- **`get_changed_files(base: str = "HEAD~1", head: str = "HEAD") -> List[str]`**
  Retrieves a list of files modified, added, or renamed between two specific commits.
  - **Parameters:**
    - `base`: The starting commit hash or reference (default is `HEAD~1`).
    - `head`: The ending commit hash or reference (default is `HEAD`).
  - **Returns:** A list of strings representing file paths relative to the repository root.

- **`get_root_dir() -> str`**
  Returns the absolute path to the root of the Git repository. If not in a repository, returns the current working directory.

---

## Logger

The `autodoc.utils.logger` module provides a standardized logging configuration for the application.

### Functions

#### `setup_logger(name="autodoc")`

Initializes and configures a logger instance with both console and file output.

- **Parameters:**
  - `name`: The name of the logger (default is `"autodoc"`).
- **Functionality:**
  - Creates the directory `.autodoc/logs/` if it does not exist.
  - **Console Output**: Logs messages to standard output.
  - **File Output**: Writes logs to `.autodoc/logs/autodoc.log`.
  - **Log Rotation**: The file handler rotates at 1MB and maintains up to 3 backup files.
  - **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Returns:** A configured `logging.Logger` object.