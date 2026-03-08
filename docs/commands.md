# CLI Commands

The `commands` module provides the primary functional logic for the Auto-Doc CLI. It handles the initialization of the Auto-Doc environment in a repository and the synchronization process that triggers AI-driven documentation updates.

## Table of Contents
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
    - [init_project](#init_project)
    - [sync_docs](#sync_docs)
- [Examples](#examples)

---

## Core Concepts

The CLI provides two main workflows:

1.  **Initialization (`init`)**: Sets up the necessary infrastructure within a local git repository. This includes creating a `.autodoc/` directory for configuration and templates, and installing a Git `post-commit` hook. The hook is "locked" to the specific Python interpreter used during initialization (`sys.executable`) to ensure stability across different virtual environments (Conda, Poetry, Venv) and operating systems.
2.  **Synchronization (`sync`)**: Analyzes the current state of the repository. It identifies changed files and commit metadata via Git, compares them against the defined `mappings` in `config.yaml`, and sends relevant code snippets to the Gemini model for documentation generation.

---

## API Reference

### `init_project()`
Installs the Auto-Doc environment and git hook in the current repository.

**Logic:**
- **Environment Check**: Verifies the presence of a `.git` directory before proceeding.
- **Git Hook**: Creates or overwrites `.git/hooks/post-commit`. 
    - It captures the absolute path of the current Python interpreter to ensure the hook executes within the correct environment.
    - The hook is a shell script that runs `python -m autodoc.hooks.post_commit` and provides feedback if the execution fails.
- **Templates**: Extracts standard Jinja2 templates from the package resources into `.autodoc/templates/` using `importlib.resources`. 
    - `system_instruction.j2`: Defines the AI's persona.
    - `doc_prompt.j2`: The structure for documentation generation requests.
    - `doc_skeleton.j2`: Used for initializing new documentation files.
    - Includes a fallback mechanism to locate templates relative to the source code for development environments.
- **Configuration**: Creates a default `.autodoc/config.yaml` if one does not exist. The default configuration includes:
    - `base_dir`: Set to `.` (project root).
    - `context`: Includes `README.md` as global context.
    - `mappings`: A default mapping for `src/**/*.py` targeting `docs/reference.md`.
    - `model`: Defaults to `gemini-3-flash-preview` with a `high` thinking level.

[source](../autodoc/commands/init.py)

---

### `sync_docs(repo_path=".")`
Manually triggers the analysis and documentation update process. This is the same logic executed automatically by the git post-commit hook.

**Parameters:**
- `repo_path` (*str*): The path to the root of the git repository. Defaults to the current directory.

**Logic:**
1.  **Change Detection**: Uses internal git utilities to identify files changed in the most recent commit and retrieves the commit message.
2.  **Mapping & Routing**:
    - Evaluates changed files against the `mappings` defined in the configuration.
    - **Priority Rule**: Matches are evaluated top-to-bottom; the first mapping that matches a file's glob pattern takes ownership.
    - **Exclusions**: If a mapping defines an `exclude` list, files matching those patterns are ignored for that specific mapping.
3.  **Generation**: Groups source files by their target documentation file. For each target, it invokes the `DocGenerator` to synthesize the changes into the documentation using the configured Gemini model.

---

## Examples

### Initialize a project
To set up Auto-Doc in a new repository:
```bash
autodoc init
```

### Manual Sync
If you want to force a documentation update without committing (e.g., to test your configuration or catch up on missed changes):
```bash
autodoc sync
```

### Routing and Exclusions Example
Given a configuration like this:
```yaml
mappings:
  - name: "Internal Utilities"
    source: "src/utils/*.py"
    exclude: ["src/utils/private_*.py"]
    doc: "docs/utils.md"
  - name: "Catch-All"
    source: "src/**/*.py"
    doc: "docs/general.md"
```

- `src/utils/string_helper.py` -> Routes to `docs/utils.md`.
- `src/utils/private_api.py` -> Matches the "Internal Utilities" source, but is **excluded**. It falls through to the "Catch-All" mapping and routes to `docs/general.md`.
- `src/core/logic.py` -> Skips the first mapping and routes to `docs/general.md`.