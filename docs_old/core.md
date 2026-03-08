# Core Logic Documentation

The `DocGenerator` class is the heart of the Auto-Doc system. It orchestrates the process of reading source files, gathering global context, prompting the Gemini AI, and updating the target documentation files.

## `DocGenerator` Class

The `DocGenerator` is responsible for the end-to-end documentation lifecycle for a specific mapping.

### Initialization

```python
def __init__(self, config: Config):
```

- **`config`**: An instance of the `Config` class containing user settings (model, context, templates).
- **Behavior**: Initializes the `GeminiClient`. If the `GEMINI_API_KEY` is missing or invalid, it logs a warning and the generator will skip updates during `update_docs`.

### Public Methods

#### `update_docs`

This is the primary entry point for generating or updating a documentation file.

```python
def update_docs(self, source_files: list, doc_target: str, git_context: dict = None):
```

- **`source_files`**: A list of file paths (resolved from glob patterns) that provide the source code context.
- **`doc_target`**: The path to the Markdown file that will be created or updated.
- **`git_context`**: (Optional) A dictionary containing metadata about the current git commit (e.g., commit message, author, diff summary) to provide the AI with change-specific context.

**Workflow:**
1.  **Read Content**: Loads the content of all provided source files.
2.  **Gather Context**: Loads "Global Context" files (e.g., `README.md`) defined in the configuration.
3.  **Load Existing Doc**: If the `doc_target` already exists, its current content is read to allow the AI to perform incremental updates.
4.  **Template Rendering**: 
    - Renders the **User Prompt** using the configured `prompt_template` or the default `autodoc/templates/default_prompt.j2`. Passes `sources`, `context_files`, `doc_content`, and `git_context` into the template.
    - Renders the **System Instruction** (the "persona") using the configured `system_instruction_template` or the default `autodoc/templates/system_instruction.j2`.
5.  **AI Generation**: Calls the Gemini API with the rendered prompt, system instructions, and the configured `thinking_level`.
6.  **Response Cleaning**: Strips markdown code fences (e.g., ```markdown ... ```) from the AI's response to ensure valid file output.
7.  **File Write**: Ensures the target directory exists and writes the generated content to the `doc_target`.

### Internal Helper Methods

#### `_render_template`

Handles the logic for loading and rendering Jinja2 templates.

```python
def _render_template(self, config_path, default_path, **kwargs) -> str:
```

- **Priority**: It first attempts to load a template from the user-defined `config_path`. If that is not set or the file does not exist, it falls back to the `default_path` provided by the Auto-Doc installation.
- **Context**: Accepts arbitrary keyword arguments to pass into the Jinja2 context.

#### `_clean_markdown_response`

Ensures the AI output is suitable for a file write.

```python
def _clean_markdown_response(self, text: str) -> str:
```

- **Logic**: If the AI wraps its entire response in Markdown code blocks (e.g., ` ```markdown ... ``` `), this method strips the opening and closing fences to prevent nested formatting issues in the final `.md` file.

#### `_read_files_with_content`

A utility to batch-read files into a format structured for the AI prompt.

```python
def _read_files_with_content(self, file_paths: list) -> list[dict]:
```

- **Return**: A list of dictionaries, each containing the `path` and the `content` of the file. If a file path does not exist, it is silently skipped.