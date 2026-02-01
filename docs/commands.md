# CLI Commands

This page provides a reference for the core commands available in the Auto-Doc system. These commands manage the lifecycle of automated documentation, from project initialization to manual or hook-triggered synchronization.

## `init_project`

Initializes the current repository to work with Auto-Doc. This command is typically run once when setting up the tool.

### Functionality
- **Git Hook Installation**: Installs a `post-commit` executable script in `.git/hooks/`. This script automatically triggers the documentation update process every time you commit changes.
- **Configuration Scaffolding**: Creates a `.autodoc/` directory and a default `config.yaml` file if they do not already exist.
- **Validation**: Ensures the command is being run inside a valid Git repository.

### Default Configuration Created
The `init` command generates a template `config.yaml` with the following defaults:
- **Global Context**: Includes `README.md` to provide the LLM with a project overview.
- **Default Mapping**: Maps Python files in `src/` to `docs/reference.md`.
- **Model Selection**: Defaults to `gemini-3-flash-preview`.

---

## `sync_docs`

The core logic engine that analyzes changes and updates documentation files. This function is called automatically by the git hook, but can also be invoked programmatically.

### Parameters
- **`repo_path`** (string): The path to the repository root. Defaults to the current directory (`"."`).

### Workflow
1. **Configuration Loading**: Reads the `.autodoc/config.yaml` to determine mapping rules and model settings.
2. **Git Analysis**: Detects which files have changed in the local repository.
3. **Mapping & Routing**: 
    - Compares changed files against the `source` glob patterns defined in the config.
    - Groups changes by their target documentation (`doc`) file.
    - Implements a priority rule where the first matching mapping takes precedence.
4. **AI Generation**: For every documentation target that has changed source files, it triggers the `DocGenerator` to analyze the code and rewrite the corresponding markdown file.

### Logic Constraints
- If no changes are detected via Git, the process exits silently.
- If changed files do not match any patterns in the configuration, no documentation updates are performed.