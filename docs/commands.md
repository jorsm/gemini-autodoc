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

1.  **Initialization (`init`)**: Sets up the necessary infrastructure within a local git repository. This includes creating a `.autodoc/` directory for configuration and templates, and installing a Git `post-commit` hook. The hook is "locked" to the Python interpreter used during initialization to ensure stability across different virtual environments (Conda, Poetry, Venv).
2.  **Synchronization (`sync`)**: Analyzes the current state of the repository. It identifies changed files and commit metadata via Git, compares them against the defined `mappings` in `config.yaml`, and sends relevant code snippets to the Gemini model for documentation generation.

---

## API Reference

### `init_project()`
Installs the Auto-Doc environment and git hook in the current repository.

**Logic:**
- **Git Hook**: Creates or overwrites `.git/hooks/post-commit`. It captures `sys.executable` to ensure the hook runs using the same Python environment where Auto-Doc was installed.
- **Templates**: Generates default Jinja2 templates in `.autodoc/templates/`:
    - `system_instruction.j2`: Defines the persona and core rules for the AI.
    - `doc_prompt.j2`: Defines the specific prompt structure used when requesting documentation updates.
- **Configuration**: Creates a default `.autodoc/config.yaml` if one does not already exist, pre-configured with standard defaults for Gemini models and basic source mappings.

[source](../autodoc/commands/init.py)

---

### `sync_docs(repo_path=".")`
Manually triggers the analysis and documentation update process. This is the same logic executed by the git hook.

**Parameters:**
- `repo_path` (*str*): The path to the root of the git repository. Defaults to the current directory.

**Logic:**
1.  **Change Detection**: Uses `GitHandler` to identify files changed in the most recent commit and retrieves the commit message/context.
2.  **Mapping & Routing**:
    - Evaluates changed files against the `mappings` defined in the configuration.
    - **Priority Rule**: Matches are evaluated top-to-bottom; the first mapping that matches a file's glob pattern takes ownership of that file.
    - **Exclusions**: If a mapping defines an `exclude` list, files matching those patterns are skipped even if they match the primary `source` glob.
    - Pattern matching follows `gitwildmatch` specifications (standard `.gitignore` style).
3.  **Generation**: Groups source files by their target documentation file. For each target, it invokes the `DocGenerator` to synthesize the changes into the documentation.

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