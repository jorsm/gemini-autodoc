# CLI Commands

This page provides a reference for the core commands available in the Auto-Doc system. These commands manage the lifecycle of automated documentation, from project initialization to manual or hook-triggered synchronization.

## `init_project`

Initializes the current repository to work with Auto-Doc. This command is typically run once when setting up the tool.

### Functionality
- **Git Hook Installation**: Installs a `post-commit` script in `.git/hooks/`. This is a Python-based hook that imports and runs `autodoc.hooks.post_commit.main`. It includes error handling to notify the user if the `autodoc` package is missing from the environment.
- **Template Scaffolding**: Creates a `.autodoc/templates/` directory containing default Jinja2 templates:
    - `system_instruction.j2`: Defines the AI's persona as an expert technical writer and sets guidelines for accuracy and Markdown formatting.
    - `doc_prompt.j2`: Defines the structure of the prompt sent to the AI, including global context, changed source code, and existing documentation.
- **Configuration Scaffolding**: Creates a default `.autodoc/config.yaml` file if it does not already exist.
- **Validation**: Verifies that the command is executed within a valid Git repository before proceeding.

### Default Configuration Created
The `init` command generates a `config.yaml` with the following defaults:
- **Global Context**: Configured to include `README.md` to provide the LLM with project-level context.
- **Mappings**: Maps all Python files (`src/**/*.py`) to `docs/reference.md`.
- **Templates**: Links to the newly created `.j2` files in the `.autodoc/templates/` directory.
- **Model Configuration**:
    - **Model**: `gemini-3-flash-preview`
    - **Thinking Level**: `high`

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
4. **AI Generation**: For every documentation target that has changed source files, it triggers the `DocGenerator` to analyze the code and rewrite the corresponding markdown file using the configured Jinja2 templates.

### Logic Constraints
- If no changes are detected via Git, the process exits silently.
- If changed files do not match any patterns in the configuration, no documentation updates are performed.