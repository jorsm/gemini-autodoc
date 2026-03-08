# Configuration Reference

The `.autodoc/config.yaml` file is the central command center for the Auto-Doc Agent. It defines which source files are analyzed, where documentation is generated, and how the AI model should reason about your code changes.

## Global Context

The `context` section provides the AI with persistent information included in every request. This ensures the agent understands the "big picture" of your project.

```yaml
context:
  files:
    - "README.md"
    - "docs/architecture.md"
```

- **`files`**: A list of paths (relative to the repository root) to files providing high-level project context. 
    - **Usage**: Include READMEs, architecture overviews, or style guides. 
    - **Benefit**: Helps the AI maintain a consistent tone and follow project-wide conventions.

---

## Mappings (File Routing)

Mappings define the relationship between your source code and your documentation files. You can create multiple mappings to split documentation into different modules, services, or layers.

> [!IMPORTANT]
> **Priority Rule**: Mappings are evaluated from **top to bottom**. Once a source file matches a `source` glob pattern, it is assigned to that mapping's `doc` file, and the agent **stops checking further mappings**. This prevents redundant updates and ensures a single file change doesn't trigger multiple AI generations.

```yaml
mappings:
  - name: "Main API"
    source: "src/**/*.py"
    doc: "docs/reference.md"
    exclude:
      - "src/tests/**"
      - "src/internal/legacy_*.py"
```

- **`name`**: A descriptive label for the mapping (used in logs).
- **`source`**: A glob pattern identifying the source files to watch.
    - Supports standard wildcards (`*`, `?`).
    - Supports recursive matching with `**` (e.g., `src/**/*.py` matches all Python files in the directory tree).
- **`doc`**: The target documentation file (Markdown) where the AI will write the updates.
- **`exclude`** *(Optional)*: A list of glob patterns to ignore. Files matching these will be skipped, even if they match the `source` pattern.

---

## Model Configuration

This section configures the underlying Google Gemini LLM.

```yaml
model: "gemini-3-flash-preview"
thinking_level: "high"
```

- **`model`**: The specific Gemini model ID.
    - **`gemini-3-flash-preview`**: (Recommended) Fast performance and a massive context window.
    - **`gemini-3-pro-preview`**: Best for extremely complex logic and deep architectural reasoning.
- **`thinking_level`**: (Gemini 3 models only) Controls the depth of reasoning performed by the model.
    - **Flash options**: `minimal`, `low`, `medium`, `high`.
    - **Pro options**: `low`, `high`.
    - **Default**: `high` (Enables dynamic reasoning). Higher levels result in a better understanding of complex logic but may increase processing time.

---

## Template Configuration

Auto-Doc uses Jinja2 templates to construct the prompts sent to Gemini. You can override the default behavior by providing paths to your own `.j2` files relative to the project root.

```yaml
prompt_template: ".autodoc/templates/doc_prompt.j2"
system_instruction_template: ".autodoc/templates/system_instruction.j2"
```

### 1. Prompt Template
Controls the structure of the specific request sent to the AI for a documentation update.
- **Available Variables**: 
    - `{{ sources }}`: The content of the source files currently being documented.
    - `{{ context_files }}`: The content of the files defined in the global context.
    - `{{ doc_file }}`: The path to the target documentation file.
    - `{{ doc_content }}`: The existing content of the target documentation file.

### 2. System Instruction Template
Defines the "Persona" and base rules for the agent. Use this to enforce specific documentation standards (e.g., "Always use Google-style docstrings" or "Ensure all technical terms link to the internal glossary").