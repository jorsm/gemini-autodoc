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
- **Template Rendering**: Uses Jinja2 for all AI communication. It follows a priority system: if a custom template path is provided in the configuration, it is used; otherwise, it falls back to the internal default templates.
- **File Management**: Reading source code, generating relative links for documentation cross-referencing, and safely writing updated Markdown files.

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
- **Behavior**: Instantiates a `GeminiClient`. If the API key is missing, it logs a warning and disables generation.

#### `update_docs(self, source_files: list, doc_target: str, git_context: dict = None)`
Updates or creates a documentation file based on provided source files.
- **Parameters**:
    - `source_files`: A list of paths to the source code files.
    - `doc_target`: The path to the Markdown file to be updated.
    - `git_context`: (Optional) Metadata about the git commit (e.g., commit message, diff summary).
- **Workflow**:
    1. **Source Loading**: Reads source files and calculates relative links from the doc target to the source code.
    2. **Context Gathering**: Loads global context files specified in the configuration.
    3. **Content Preparation**: If the target exists, it reads the current content. If not, it generates a new document skeleton using `autodoc/templates/doc_skeleton.j2`.
    4. **Prompt Construction**: Renders the system instruction and the user prompt using Jinja2 templates (`system_instruction.j2` and `default_prompt.j2`).
    5. **AI Generation**: Sends the data to the Gemini API with the configured `thinking_level`.
    6. **Post-Processing**: Strips Markdown code block wrappers from the AI response and writes the cleaned content to the filesystem.

---

### `GeminiClient`
A wrapper around the Google GenAI SDK for interacting with Gemini models.

#### `__init__(self, api_key: str = None, model: str = "gemini-3.0-flash")`
Sets up the GenAI client.
- **Parameters**:
    - `api_key`: (Optional) The Google API key. If omitted, it attempts to load from `GEMINI_API_KEY` environment variable or `.env` file.
    - `model`: The specific Gemini model identifier (default: `gemini-3.0-flash`).
- **Raises**: `ValueError` if no API key is found.

#### `generate_documentation(self, prompt: str, system_instruction: str = None, thinking_level: str = "high") -> str`
Sends a generation request to the model with specific reasoning configurations.
- **Parameters**:
    - `prompt`: The user-level instructions and data.
    - `system_instruction`: (Optional) The persona or high-level constraints for the model.
    - `thinking_level`: The reasoning depth (`"minimal"`, `"low"`, `"medium"`, or `"high"`).
- **Returns**: The generated Markdown text.
- **Details**: Uses `include_thoughts=False` to return only the final documentation output while utilizing the model's internal reasoning process.

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
The `DocGenerator` automatically handles AI "chattiness" by stripping Markdown wrappers:

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