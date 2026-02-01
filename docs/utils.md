# Utilities

This page provides documentation for the utility modules used within the Auto-Doc system to handle version control operations and logging.

## Git Handler

The `autodoc.utils.git_handler` module provides a wrapper around `GitPython` to manage repository interactions and track file changes.

### `GitHandler` Class

Handles interactions with the local Git repository.

#### Methods

- **`__init__(repo_path: str = ".")`**
  Initializes the handler.
  - **Parameters:**
    - `repo_path`: Path to the git repository (default is the current directory).
  - **Behavior:** If the path is not a valid Git repository, the internal `repo` attribute is set to `None`.

- **`get_changed_files(base: str = "HEAD~1", head: str = "HEAD") -> List[str]`**
  Retrieves a list of files modified, added, or renamed between two specific commits.
  - **Parameters:**
    - `base`: The starting commit hash or reference (default is `HEAD~1`).
    - `head`: The ending commit hash or reference (default is `HEAD`).
  - **Returns:** A list of strings representing file paths relative to the repository root. 
  - **Behavior:** 
    - Returns an empty list if the repository is invalid or if the `base` commit cannot be found (e.g., in an initial commit scenario).
    - Filters changes to include only Added (`A`), Modified (`M`), and Renamed (`R`) files.

- **`get_root_dir() -> str`**
  Returns the absolute path to the root of the Git repository.
  - **Returns:** The `working_dir` of the repository if it exists, otherwise the current working directory.

---

## Logger

The `autodoc.utils.logger` module provides a standardized logging configuration for the application.

### Functions

#### `setup_logger(name="autodoc")`

Initializes and configures a logger instance with both console and rotating file output.

- **Parameters:**
  - `name`: The name of the logger (default is `"autodoc"`).
- **Functionality:**
  - **Directory Management**: Automatically creates the `.autodoc/logs/` directory if it does not exist.
  - **Deduplication**: Checks for existing handlers to avoid duplicate log entries if called multiple times.
  - **Level**: Sets the logging level to `INFO`.
  - **Console Output**: Logs messages to standard output via a `StreamHandler`.
  - **File Output**: Writes logs to `.autodoc/logs/autodoc.log` using a `RotatingFileHandler`.
  - **Log Rotation**: Files rotate once they reach 1MB, keeping a maximum of 3 backup files.
  - **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Returns:** A configured `logging.Logger` object.