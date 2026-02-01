# Core Engine

The `autodoc.core` module contains the primary logic for analyzing source code and generating documentation updates using AI.

## DocGenerator Class

The `DocGenerator` class is the central orchestrator of the documentation workflow. It handles file I/O, prompt construction via Jinja2 templates, and communication with the Gemini API.

### Initialization

```python
DocGenerator(config: Config)
```

- **config**: An instance of `autodoc.config.Config` containing model settings, context file paths, and template configurations.
- The constructor initializes the `GeminiClient` using the model specified in the configuration. If the API key is missing or invalid, it logs a warning and disables generation.

### Public Methods

#### `update_docs`

The main entry point for triggering a documentation refresh.

```python
def update_docs(self, source_files: list, doc_target: str):
```

- **source_files**: A list of paths to source code files that have changed.
- **doc_target**: The path to the markdown file that should be updated (e.g., `docs/API.md`).

**Process Flow:**
1.  **Validation**: Checks if the AI client is initialized.
2.  **Source Gathering**: Reads the content of the modified source files.
3.  **Global Context**: Reads content from additional context files specified in `config.context["files"]`.
4.  **State Analysis**: Reads the current content of the `doc_target` to allow for incremental updates.
5.  **Prompt & System Instruction Construction**: Uses the internal `_render_template` method to build the prompt and the system instructions.
6.  **AI Generation**: Sends the data to the Gemini API, passing the `thinking_level` defined in the configuration.
7.  **Post-Processing**: Strips markdown code blocks (backticks) from the AI's response to ensure only raw markdown is saved.
8.  **File Write**: Ensures the target directory exists and writes the updated content to disk.

### Internal Logic

#### Template Rendering (`_render_template`)
The generator uses **Jinja2** templates to construct both the user prompt and the system instruction. It follows a specific priority for resolving template files:
1.  **Configured Path**: Uses the path defined in the configuration (e.g., `config.prompt_template`).
2.  **Default Internal Path**: If no custom path is provided or the file is missing, it falls back to internal defaults (e.g., `autodoc/templates/default_prompt.j2` or `autodoc/templates/system_instruction.j2`).

#### System Instruction
The system instruction is dynamically rendered from a template. It defines the AI's persona as an expert technical writer and provides constraints to ensure:
- Accurate reflection of the source code.
- Preservation of existing markdown structures.
- Return of raw markdown content only.
- A hardcoded fallback instruction is provided if no template files are found.