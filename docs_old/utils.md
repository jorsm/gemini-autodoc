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

- **`get_commit_context(commit: str = "HEAD") -> dict`**
  Retrieves metadata and context for a specific commit.
  - **Parameters:**
    - `commit`: The commit hash or reference to query (default is `HEAD`).
  - **Returns:** A dictionary containing:
    - `hash`: The full SHA-1 hash of the commit.
    - `message`: The commit message (stripped of leading/trailing whitespace).
    - `author`: The name of the commit author.
    - `author_email`: The email of the commit author.
    - `date`: The ISO 8601 formatted string of the commit date.
  - **Behavior:** Returns an empty dictionary if the repository is invalid or if the commit reference cannot be resolved.

- **`get_root_dir() -> str`**
  Returns the absolute path to the root of the Git repository.
  - **Returns:** The `working_dir` of the repository if it exists, otherwise the current working directory.

---

## Logger

The `autodoc.utils.logger` module provides a standardized logging configuration for the application, ensuring that execution details are captured for both real-time monitoring and debugging.

### Functions

#### `setup_logger(name="autodoc")`

Initializes and configures a logger instance with both console and rotating file output.

- **Parameters:**
  - `name` (str): The name of the logger instance. Defaults to `"autodoc"`.
- **Functionality:**
  - **Directory Management**: Ensures the `.autodoc/logs/` directory exists, creating it if necessary.
  - **Deduplication**: Checks `logger.handlers` to prevent adding redundant handlers if the setup function is called multiple times.
  - **Level**: Sets the logging level to `INFO`.
  - **Format**: Uses a standardized format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.
  - **Console Output**: Configures a `StreamHandler` to output logs to the terminal.
  - **File Output**: Configures a `RotatingFileHandler` pointing to `.autodoc/logs/autodoc.log`.
  - **Log Rotation**: Implements automatic rotation when the log file reaches **1MB** (`maxBytes=1024 * 1024`), maintaining a maximum of **3** backup files.
- **Returns:** 
  - `logging.Logger`: A fully configured logger instance.

```python
from autodoc.utils.logger import setup_logger

logger = setup_logger("my_app")
logger.info("Auto-Doc is running.")
```