# Phase 3: Smart Context & Mapping

## 1. Configuration Upgrade and File Routing
**Goal**: Support complex project structures by mapping source files to documentation files.

- [ ] **Config Schema Update**:
    - Update `Config` class to support `context` (global files) and `mappings` keys.
    - Example Schema:
      ```yaml
      context:
        files: ["README.md"]
      mappings:
        - name: "Core API"
          source: "src/**/*.py"
          doc: "docs/API.md"
      ```
- [ ] **Path Matching Logic**:
    - Implement glob matching to route changed files to the correct mapping rule.
- [ ] **DocGenerator Context**:
    - Update `DocGenerator` to read and include `context.files` in the prompt.

## 2. Intelligent Context Engine (AST Pruning)
**Goal**: Solve the "2000 lines" problem by sending only relevant code.

- [ ] **Diff Analysis**:
    - Extend `GitHandler` to return modified line numbers for each file.
- [ ] **AST Pruner**:
    - Create `autodoc/core/pruner.py`.
    - Logic: Parse file -> Identify changed functions/classes -> Replace unchanged bodies with `...` or signatures.

## 3. Orchestration
**Goal**: Tie it all together.

- [ ] **Sync Logic**:
    - Loop logic: Changed File -> Find Mapping -> Prune Content -> Generate Prompt -> Update Doc.
    - Batching: If 3 files map to `API.md`, combine them into one update request (optional optimization).
