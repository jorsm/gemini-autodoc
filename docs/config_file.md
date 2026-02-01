# Configuration Reference

The `.autodoc/config.yaml` file controls how the Auto-Doc Agent behaves. It defines which source files are analyzed, where the documentation is written, and how the AI model should reason about your code.

## Global Context

The `context` section allows you to provide the AI with persistent information that is included in every request.

```yaml
context:
  files:
    - "README.md"
    - "docs/architecture.md"
```

- **`files`**: A list of paths (relative to the repository root) to files that provide high-level project context. Use this for READMEs, architecture overviews, or style guides. This ensures the AI understands the overall project goal and maintains a consistent tone.

---

## Mappings (File Routing)

Mappings define the relationship between your source code and your documentation files. You can create multiple mappings to split documentation into different modules or layers.

```yaml
mappings:
  - name: "Main API"
    source: "src/**/*.py"
    doc: "docs/reference.md"
    exclude:
      - "src/tests/**"
      - "src/internal/legacy_*.py"
```

- **`name`**: A descriptive name for the mapping (used for logging and internal reference).
- **`source`**: A glob pattern identifying the source files to watch.
    - Supports standard wildcards (`*`, `?`).
    - Supports recursive matching with `**` (e.g., `src/**/*.py` matches all Python files in `src` and all subdirectories).
- **`doc`**: The target documentation file (Markdown) where the generated content will be written.
- **`exclude`** *(Optional)*: A list of glob patterns to ignore. Files matching these patterns will not be sent to the AI for analysis, even if they match the `source` pattern.

---

## Model Configuration

This section configures the underlying Google Gemini LLM.

```yaml
model: "gemini-3-flash-preview"
thinking_level: "high"
```

- **`model`**: The specific Gemini model ID to use. 
    - Recommended: `gemini-3-flash-preview` for high speed and a massive context window.
    - Alternatives: `gemini-3-pro-preview` for extremely complex logic and deepest reasoning.
- **`thinking_level`**: (Gemini 3 models only) Controls the depth of reasoning performed by the model.
    - **Flash options**: `minimal`, `low`, `medium`, `high`.
    - **Pro options**: `low`, `high`.
    - **Default**: `high`. Higher levels result in better understanding of complex logic but may increase processing time.

---

## Template Configuration

Auto-Doc uses Jinja2 templates to construct the prompts sent to Gemini. You can override the default templates by providing paths to your own `.j2` files relative to the project root.

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
    - `{{ doc_content }}`: The existing content of the target documentation file (allowing for incremental updates).

### 2. System Instruction Template
Defines the "Persona" and base rules for the agent. Use this to set strict requirements for documentation format (e.g., "Always use Google-style docstrings" or "Ensure all Mermaid diagrams are valid").