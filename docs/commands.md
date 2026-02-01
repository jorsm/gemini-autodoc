# CLI Commands

This page provides a reference for the core commands available in the Auto-Doc system. These commands manage the lifecycle of automated documentation, from project initialization to manual or hook-triggered synchronization.

## `init_project`

Initializes the current repository to work with Auto-Doc by setting up the necessary git hooks, configuration files, and Jinja2 templates.

### Functionality
- **Git Hook Installation**: Installs a `post-commit` shell script in `.git/hooks/`. 
    - **Environment Locking**: The script captures the path of the Python interpreter used to run the `init` command (`sys.executable`). This ensures that the hook always runs within the correct virtual environment (Conda, Poetry, `.venv`, etc.) regardless of how the Git commit is triggered (terminal or IDE).
    - It executes the hook logic via `"{python_exe}" -m autodoc.hooks.post_commit`.
- **Template Scaffolding**: Creates a `.autodoc/templates/` directory and populates it with default Jinja2 templates extracted from the package resources:
    - `system_instruction.j2`: Defines the AI's persona as an expert technical writer and sets guidelines for accuracy and Markdown structure.
    - `doc_prompt.j2`: The primary prompt template used to send context, source code, and existing documentation to the Gemini model.
- **Configuration Scaffolding**: Generates a default `.autodoc/config.yaml` file to define mapping rules and model parameters.
- **Validation**: Ensures the command is run inside a valid Git repository root.

### Default Configuration Created
The `init` command generates a `config.yaml` with the following defaults:
- **Global Context**: Includes `README.md` to provide the LLM with high-level project information.
- **Mappings**: Maps all Python files in `src/` (`src/**/*.py`) to a target documentation file at `docs/reference.md`.
- **Templates**: Paths are set to the local `.autodoc/templates/` folder.
- **Model Configuration**:
    - **Model**: `gemini-3-flash-preview`
    - **Thinking Level**: `high`

---

## `sync_docs`

The core synchronization engine that analyzes recent repository changes and triggers documentation updates. While usually invoked automatically by the Git post-commit hook, it can also be triggered manually or via CI/CD.

### Parameters
- **`repo_path`** (string): The path to the repository root. Defaults to the current directory (`"."`).

### Workflow
1. **Configuration Loading**: Initializes settings from `.autodoc/config.yaml` and sets the active repository path.
2. **Change Detection**: Uses a `GitHandler` to identify files modified in the latest commit. If no changes are detected, the process exits gracefully.
3. **Mapping & Routing**:
    - Iterates through detected changes and matches them against `source` glob patterns.
    - **Exclusion Logic**: Checks an optional `exclude` list for each mapping. If a file matches an exclusion pattern, it is skipped for that mapping.
    - **Resolution**: Resolves paths to ensure accurate matching using `Path.match`.
    - **Grouping**: Groups changed source files by their respective target `doc` file.
    - **Priority Rule**: Only the first matching (and non-excluded) mapping for a file is processed.
4. **AI-Driven Update**: For each target documentation file, it invokes the `DocGenerator`. This component uses the Gemini API and the configured Jinja2 templates to rewrite the documentation based on the updated source code logic.

### Logic Constraints
- **Empty Commits**: If no files have changed according to Git, the process terminates without taking action.
- **Mapping Coverage**: Only files matching the `source` globs defined in `config.yaml` trigger updates.
- **Logging**: Provides real-time feedback via the internal logger regarding detected changes, environment detection, and AI status.