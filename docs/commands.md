# CLI Commands

This page provides a reference for the core commands available in the Auto-Doc system. These commands manage the lifecycle of automated documentation, from project initialization to manual or hook-triggered synchronization.

## `init_project`

Initializes the current repository to work with Auto-Doc by setting up necessary hooks, configuration files, and templates.

### Functionality
- **Git Hook Installation**: Installs a `post-commit` script in `.git/hooks/`. This hook is a Python script that attempts to import and execute `autodoc.hooks.post_commit.main`. It includes built-in checks to ensure `autodoc` is installed in the active environment.
- **Template Scaffolding**: Creates a `.autodoc/templates/` directory containing default Jinja2 templates:
    - `system_instruction.j2`: Defines the AI's persona as an expert technical writer and sets specific guidelines for accuracy, Markdown structure, and clarity.
    - `doc_prompt.j2`: Defines the prompt structure, passing `context_files`, `sources` (changed files), and existing `doc_content` to the model.
- **Configuration Scaffolding**: Generates a default `.autodoc/config.yaml` file to define how source files map to documentation files.
- **Validation**: Ensures the command is run inside a valid Git repository before attempting installation.

### Default Configuration Created
The `init` command generates a `config.yaml` with the following defaults:
- **Global Context**: Includes `README.md` to provide the LLM with high-level project information.
- **Mappings**: Maps all Python files in `src/` (`src/**/*.py`) to `docs/reference.md`.
- **Templates**: Configured to use the local `.autodoc/templates/` directory.
- **Model Configuration**:
    - **Model**: `gemini-3-flash-preview`
    - **Thinking Level**: `high`

---

## `sync_docs`

The core synchronization engine that analyzes recent repository changes and triggers documentation updates. This function is invoked automatically by the Git post-commit hook but can also be called manually.

### Parameters
- **`repo_path`** (string): The path to the repository root. Defaults to the current directory (`"."`).

### Workflow
1. **Configuration Loading**: Initializes settings from `.autodoc/config.yaml`, determining mapping rules and model parameters.
2. **Change Detection**: Uses a `GitHandler` to identify files that have been modified in the latest commit.
3. **Mapping & Routing**:
    - Iterates through detected changes and matches them against `source` glob patterns defined in the configuration.
    - Resolves absolute paths to ensure accurate pattern matching using `Path.match`.
    - Groups changed source files by their respective target documentation (`doc`) file.
    - **Priority Rule**: Only the first matching mapping for a file is processed.
4. **AI-Driven Update**: For each target documentation file identified, it invokes the `DocGenerator`. The generator uses the configured Jinja2 templates and the Gemini API to rewrite the documentation based on the new source code logic.

### Logic Constraints
- If no files have changed according to Git, the process terminates without action.
- Only files matching the `source` globs defined in `config.yaml` will trigger an update. Files outside these patterns are ignored.