# Core

The `core` module contains the primary engine of Auto-Doc. It is responsible for orchestrating the documentation lifecycle: reading source code, constructing AI prompts using Jinja2 templates, communicating with the Gemini API, and writing the final documentation files.

## Table of Contents
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
    - [DocGenerator](#docgenerator)
    - [GeminiClient](#geminiclient)
- [Examples](#examples)

---

## Core Concepts

### Orchestration
The `DocGenerator` serves as the central orchestrator. It maps source files to documentation targets based on the user's configuration. It handles:
- **Context Injection**: Merging global context files (defined in `config.yaml`) into the prompt to provide the AI with project-wide knowledge.
- **Template Rendering**: Uses Jinja2 for all AI communication. It follows a strict priority system for resolving templates, allowing users to override defaults at multiple levels.
- **File Management**: Reading source code, generating relative links for documentation cross-referencing, and safely writing updated Markdown files.

### Template Resolution Priority
When rendering a template (system instructions, prompts, or skeletons), Auto-Doc searches in the following order:
1.  **Configured Path**: The specific path defined in `.autodoc/config.yaml` (e.g., `prompt_template: "custom/my_prompt.j2"`).
2.  **Local Project Default**: Files located in your project's `.autodoc/templates/` directory matching the default filename.
3.  **Internal Package Default**: The built-in templates bundled with the `autodoc` Python package.

### AI Reasoning
The `GeminiClient` interfaces with Google's Gemini models using the `google-genai` SDK. It leverages the **Thinking** capabilities of the Gemini 3.0 family, allowing the agent to perform deep reasoning about code logic and architecture. The depth of this reasoning is controlled via the `thinking_level` parameter.

---

## API Reference

### `DocGenerator`
The main class responsible for the end-to-end documentation update process.

#### `__init__(self, config: Config)`
Initializes the generator with a project configuration.
- **Parameters**:
    - `config`: A `Config` object containing model settings, mappings, and template paths.
- **Behavior**: Instantiates a `GeminiClient`. If the API key is missing, it logs a warning and disables generation functionality for the session.

#### `update_docs(self, source_files: list, doc_target: str, git_context: dict = None)`
Updates or creates a documentation file based on provided source files.
- **Parameters**:
    - `source_files`: A list of paths to the source code files.
    - `doc_target`: The path to the Markdown file to be updated.
    - `git_context`: (Optional) Metadata about the git commit (e.g., commit message, diff summary).
- **Workflow**:
    1.  **Source Loading**: Reads source files and calculates relative links from the doc target to the source code for better AI context.
    2.  **Context Gathering**: Loads global context files specified in the configuration.
    3.  **Content Preparation**: If the target exists, it reads the current content. If not, it generates a new document skeleton using `doc_skeleton.j2`.
    4.  **Prompt Construction**: Renders the system instruction and the user prompt using the template resolution logic.
    5.  **AI Generation**: Sends the data to the Gemini API using the `thinking_level` defined in the configuration.
    6.  **Post-Processing**: Strips Markdown code block wrappers (` ```markdown `) from the AI response and writes the cleaned content to the filesystem.

---

### `GeminiClient`
A wrapper around the Google GenAI SDK for interacting with Gemini models.

#### `__init__(self, api_key: str = None, model: str = "gemini-3.0-flash")`
Sets up the GenAI client.
- **Parameters**:
    - `api_key`: (Optional) The Google API key. If omitted, it attempts to load from the `GEMINI_API_KEY` environment variable or a `.env` file.
    - `model`: The specific Gemini model identifier (e.g., `gemini-3.0-flash` or `gemini-3.0-pro`).
- **Raises**: `ValueError` if no API key is found.

#### `generate_documentation(self, prompt: str, system_instruction: str = None, thinking_level: str = "high") -> str`
Sends a generation request to the model with specific reasoning configurations.
- **Parameters**:
    - `prompt`: The rendered user-level instructions and data.
    - `system_instruction`: (Optional) The persona or high-level constraints for the model.
    - `thinking_level`: The reasoning depth (`"minimal"`, `"low"`, `"medium"`, or `"high"`).
- **Returns**: The generated Markdown text.

---

## Examples

### Manual Doc Generation
You can use the core components programmatically to trigger updates outside of the standard git hook workflow:

```python
from autodoc.config import Config
from autodoc.core.doc_generator import DocGenerator

# 1. Load configuration
config = Config.load_from_file(".autodoc/config.yaml")

# 2. Initialize generator
generator = DocGenerator(config)

# 3. Update a specific doc manually
generator.update_docs(
    source_files=["autodoc/core/doc_generator.py"],
    doc_target="docs/core.md",
    git_context={"message": "docs: updating core logic documentation"}
)
```

### Response Cleaning
The `DocGenerator` automatically handles AI "chattiness" or formatting wrappers to ensure the final file is valid Markdown:

```python
# Raw AI Response:
# ```markdown
# # My Documentation
# content...
# ```

# DocGenerator._clean_markdown_response(text) returns:
# # My Documentation
# content...
```