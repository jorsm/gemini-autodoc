# Auto-Doc Refactor Implementation Plan

## Phase 1: Foundation (The Skeleton)
- [ ] **Package Structure Setup**:
    - Create `pyproject.toml` with dependencies (`google-genai`, `GitPython`, `jinja2`, `pyyaml`).
    - Create `src/autodoc` directory structure (`__init__.py`, `cli.py`, `core/`, `utils/`).
- [ ] **GitPython Integration**:
    - Implement `src/autodoc/utils/git_handler.py` using `GitPython` to replace `subprocess` calls.
- [ ] **CLI Entry Point**:
    - Implement `main` entry point in `cli.py`.
    - Register `autodoc` command in `pyproject.toml`.

## Phase 2: Logic & Architecture (The Brain)
- [ ] **Configuration Loader**:
    - Implement `src/autodoc/config.py` to load `.autodoc.yaml`.
    - Define default configuration schema.
- [ ] **Modularization**:
    - Move Gemini logic to `src/autodoc/core/gemini_client.py`.
    - Move Doc processing to `src/autodoc/core/doc_generator.py`.
- [ ] **Jinja2 Templates**:
    - Create `src/autodoc/templates/default_prompt.j2`.
    - Integrate template rendering into `doc_generator.py`.

## Phase 3: Migration & Cleanup
- [ ] **Update Hook Installer**:
    - Rewrite `install_hook.sh` (or create `install.py`) to install the tool as a package.
    - Update the git hook to call the `autodoc` CLI.
- [ ] **Cleanup**:
    - Remove old `.auto-doc` folder and scripts.
