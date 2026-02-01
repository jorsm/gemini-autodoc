# Configuration Reference

The `autodoc.yaml` (or `.autodoc/config.yaml`) file controls how the Auto-Doc Agent behaves. It defines which source files are analyzed, where the documentation is written, and how the AI model should reason about your code.

## Global Context

The `context` section allows you to provide the AI with persistent information that is included in every request.

```yaml
context:
  files:
    - "README.md"
```

- **`files`**: A list of paths to files that provide high-level project context. Use this for READMEs, architecture overviews, or style guides. This ensures the AI understands the overall project goal and tone.

---

## Mappings (File Routing)

Mappings define the relationship between your source code and your documentation files. You can create multiple mappings to split documentation into different modules.

```yaml
mappings:
  - name: "Main API"
    source: "src/**/*.py"
    doc: "docs/reference.md"
```

- **`name`**: A descriptive name for the mapping (used for logging and internal reference).
- **`source`**: A glob pattern identifying the source files to watch.
    - Supports standard wildcards (`*`, `?`).
    - Supports recursive matching with `**` (e.g., `src/**/*.py` matches all Python files in `src` and subdirectories).
- **`doc`**: The target documentation file where the generated content will be written.

---

## Model Configuration

This section configures the underlying Gemini LLM.

```yaml
model: "gemini-3-flash-preview"
thinking_level: "high"
```

- **`model`**: The specific Gemini model ID to use. 
    - Recommended: `gemini-3-flash-preview` for speed and large context windows.
    - Alternatives: `gemini-3-pro-preview` for complex logic and deeper reasoning.
- **`thinking_level`**: (Gemini 3 models only) Controls the depth of reasoning performed by the model.
    - **Flash options**: `minimal`, `low`, `medium`, `high`.
    - **Pro options**: `low`, `high`.
    - Default is `high`.

---

## Template Configuration

Auto-Doc uses Jinja2 templates to construct prompts. You can override the default templates by providing paths to your own `.j2` files.

```yaml
# prompt_template: ".autodoc/templates/doc_prompt.j2"
# system_instruction_template: ".autodoc/templates/system_instruction.j2"
```

### 1. Prompt Template
Controls the structure of the specific request sent to the AI.
- **Available Variables**: 
    - `{{ sources }}`: The content of the source files being documented.
    - `{{ context_files }}`: The content of the files defined in the global context.
    - `{{ doc_file }}`: The path to the target documentation file.
    - `{{ doc_content }}`: The existing content of the documentation file (if any).

### 2. System Instruction Template
Defines the "Persona" of the agent. Use this to set strict rules about documentation format (e.g., "Always use Google-style docstrings" or "Never include private methods").