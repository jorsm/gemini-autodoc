# Core Engine

The `autodoc.core` module contains the primary logic for analyzing source code and generating documentation updates using AI.

## DocGenerator Class

The `DocGenerator` class is the central orchestrator of the documentation workflow. It handles file I/O, prompt construction via Jinja2 templates, and communication with the Gemini API.

### Initialization

```python
DocGenerator(config: Config)
```

- **config**: An instance of `autodoc.config.Config` containing model settings, context file paths, and template configurations.
- The constructor initializes the `GeminiClient`. If the API key is missing or invalid, it logs a warning and disables generation.

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
2.  **Context Gathering**: Reads the content of the modified source files and any "global context" files defined in the configuration.
3.  **State Analysis**: Reads the current content of the `doc_target` to allow for incremental updates.
4.  **Prompt Rendering**: Combines source code, context, and current documentation into a prompt using the `_render_prompt` method.
5.  **AI Generation**: Sends the prompt to the Gemini API with a specialized "Expert Technical Writer" system instruction.
6.  **Post-Processing**: Strips markdown code blocks (backticks) from the AI's response to ensure clean file output.
7.  **File Write**: Ensures the target directory exists and writes the updated content to disk.

### Internal Logic

#### Prompt Rendering
The generator uses **Jinja2** templates to construct prompts. It follows a specific priority for templates:
1.  Custom template path defined in `config.prompt_template`.
2.  Internal default template at `autodoc/templates/default_prompt.j2`.
3.  A hardcoded fallback string if no files are found.

#### System Instruction
The generator provides a strict system instruction to the AI model to ensure:
- Accurate reflection of the source code.
- Preservation of existing markdown structures.
- Return of raw markdown content only.