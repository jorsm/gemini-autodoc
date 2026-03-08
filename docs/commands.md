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

1.  **Initialization (`init`)**: Sets up the necessary infrastructure within a local git repository. This includes creating a `.autodoc/` directory for configuration and templates, and installing a Git `post-commit` hook. The hook is "locked" to the Python interpreter used during initialization to ensure stability across different virtual environments.
2.  **Synchronization (`sync`)**: Analyzes the current state of the repository. It identifies changed files via Git, compares them against the defined `mappings` in `config.yaml`, and sends relevant code snippets to the Gemini model for documentation generation.

---

## API Reference

### `init_project()`
Installs the Auto-Doc environment and git hook in the current repository.

**Logic:**
- **Git Hook**: Creates or overwrites `.git/hooks/post-commit`. It captures `sys.executable` to ensure the hook runs using the same Python environment where Auto-Doc was installed.
- **Templates**: Generates default Jinja2 templates in `.autodoc/templates/`:
    - `system_instruction.j2`: The persona and rules for the AI.
    - `doc_prompt.j2`: The specific prompt structure for updating documentation.
- **Configuration**: Creates a default `.autodoc/config.yaml` if one does not already exist.

[source](../autodoc/commands/init.py)

---

### `sync_docs(repo_path=".")`
Manually triggers the analysis and documentation update process.

**Parameters:**
- `repo_path` (*str*): The path to the root of the git repository. Defaults to the current directory.

**Logic:**
1.  **Change Detection**: Uses `GitHandler` to find files changed in the most recent commit.
2.  **Mapping & Routing**:
    - Evaluates changed files against `mappings` defined in the config.
    - **Priority Rule**: Matches are evaluated top-to-bottom; the first mapping that matches a file's glob pattern (and is not excluded) takes ownership of that file.
    - Supports `gitwildmatch` patterns (e.g., `src/**/*.py`).
3.  **Generation**: For each documentation target identified, it collects the source code of the changed files and invokes the `DocGenerator`.

[source](../autodoc/commands/sync.py)

---

## Examples

### Initialize a project
To set up Auto-Doc in a new repository:
```bash
autodoc init
```

### Manual Sync
If you want to force a documentation update without committing, or to test your configuration:
```bash
autodoc sync
```

### Routing Logic Example
Given a configuration like this:
```yaml
mappings:
  - name: "Core"
    source: "src/core/*.py"
    doc: "docs/core.md"
  - name: "Utils"
    source: "src/**/*.py"
    doc: "docs/general.md"
```
If `src/core/logic.py` changes, it will be routed to `docs/core.md` because the "Core" mapping appears first. It will *not* be processed by the "Utils" mapping.