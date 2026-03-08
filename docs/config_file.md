# Configuration Reference

The `.autodoc/config.yaml` file is the central control point for the Auto-Doc agent. It defines the behavior of the agent, including file routing, LLM model selection, reasoning depth, and context management.

## Table of Contents
- [Overview](#overview)
- [Configuration Schema](#configuration-schema)
- [Parameter Details](#parameter-details)
- [Examples](#examples)

---

## Overview

The configuration file is structured into four functional areas:
1.  **Context**: Files that are always provided to the LLM to maintain consistency and tone.
2.  **Mappings**: Defines the routing logic between source code (via glob patterns) and documentation files.
3.  **Model Configuration**: Selects the Gemini model version and adjusts reasoning depth.
4.  **Template Configuration**: Allows overriding standard Jinja2 templates for custom output formatting.

## Configuration Schema

```yaml
context:
  files:
    - "README.md"

mappings:
  - name: "Document Name"
    source: "src/**/*.py"
    doc: "docs/output.md"
    exclude: ["src/tests/**"]

model: "gemini-3.1-flash-lite-preview"
thinking_level: "high"

# Optional template overrides
# prompt_template: ".autodoc/templates/doc_prompt.j2"
# system_instruction_template: ".autodoc/templates/system_instruction.j2"
```

## Parameter Details

### 1. Global Context (`context.files`)
A list of file paths that are injected into every prompt. Use this for style guides, high-level architecture documents, or your `README.md` to ensure the agent understands the project's purpose and tone.

### 2. Mappings (`mappings`)
An ordered list of routing rules.
*   **Priority Rule**: Mappings are evaluated **top-to-bottom**. The agent assigns a file change to the *first* configuration block that matches the source pattern.
*   **source**: A glob pattern identifying the source code files to watch (e.g., `src/**/*.py`).
*   **doc**: The specific documentation file that should be updated when the source changes.
*   **exclude**: (Optional) A list of glob patterns to ignore, preventing specific files from triggering updates.

### 3. Model & Reasoning (`model`, `thinking_level`)
*   **model**: Specifies the Google Gemini model string.
*   **thinking_level**: Controls the reasoning depth (the "Thinking" process).
    *   **Available Levels**: `"minimal"`, `"low"`, `"medium"`, `"high"`.
    *   **Constraint Logic**:
        *   **Gemini 3 Flash**: Supports all levels (`minimal`, `low`, `medium`, `high`).
        *   **Gemini 3 Pro**: Supports `low` and `high` levels.
    *   **Default**: `"high"` (Recommended for complex codebases).

### 4. Templates
*   **prompt_template**: Override the path to the `.j2` file used to structure the LLM request.
*   **system_instruction_template**: Override the path to the `.j2` file defining the AI's persona and rulebook.

## Examples

### Defining Strict Mappings
To ensure your auth logic is documented in a specific file while the rest of the API goes to a general reference, use order:

```yaml
mappings:
  - name: "Auth Docs"
    source: "src/auth/**/*.py"
    doc: "docs/auth.md"
    
  - name: "General API"
    source: "src/**/*.py"
    doc: "docs/api.md"
```
*Note: Any file in `src/auth/` will be handled by the "Auth Docs" block and ignored by "General API" due to the Priority Rule.*