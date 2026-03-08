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
- **Context Injection**: Merging global context files (like READMEs) into the prompt.
- **Template Rendering**: Using Jinja2 to allow users to customize how prompts and documentation skeletons are structured.
- **File Management**: Reading source code and safely writing updated Markdown files.

### AI Reasoning
The `GeminiClient` interfaces with Google's Gemini models. It specifically utilizes the **Thinking** capabilities of Gemini 3.0, allowing the agent to reason about code logic rather than just performing keyword matching. The `thinking_level` can be adjusted to balance speed and reasoning depth.

---

## API Reference

### `DocGenerator`
The main class responsible for the end-to-end documentation update process.

#### `__init__(self, config: Config)`
Initializes the generator with a project configuration.
- **Parameters**:
    - `config`: A `Config` object containing model settings, mappings, and template paths.
- **Side Effects**: Instantiates a `GeminiClient`. Logs a warning if the client fails to initialize (e.g., missing API key).

#### `update_docs(self, source_files: list, doc_target: str, git_context: dict = None)`
The primary method to update a specific documentation file based on a set of source files.
- **Parameters**:
    - `source_files`: A list of strings/paths to the source code files being documented.
    - `doc_target`: The path to the Markdown file to be updated or created.
    - `git_context`: (Optional) A dictionary containing metadata about the recent git commit (author, message, diff summary).
- **Logic**:
    1. Reads source files and generates relative links.
    2. Reads global context files defined in the config.
    3. Loads the existing documentation or creates a skeleton from a template.
    4. Renders the system instruction and prompt via Jinja2.
    5. Calls the Gemini API and cleans the Markdown response.
    6. Writes the result to `doc_target`. [source](../autodoc/core/doc_generator.py)

---

### `GeminiClient`
A wrapper around the Google GenAI SDK.

#### `__init__(self, api_key: str = None, model: str = "gemini-3.0-flash")`
Sets up the Google GenAI client.
- **Parameters**:
    - `api_key`: (Optional) The Google API key. If not provided, it looks for `GEMINI_API_KEY` in environment variables or `.env`.
    - `model`: The model identifier to use (default: `gemini-3.0-flash`).
- **Raises**: `ValueError` if no API key is found. [source](../autodoc/core/gemini_client.py)

#### `generate_documentation(self, prompt: str, system_instruction: str = None, thinking_level: str = "high") -> str`
Sends a request to the Gemini model to generate documentation content.
- **Parameters**:
    - `prompt`: The full user prompt containing source code and context.
    - `system_instruction`: (Optional) The system-level persona or constraints.
    - `thinking_level`: The reasoning depth for the model (`"minimal"`, `"low"`, `"medium"`, or `"high"`).
- **Returns**: The generated Markdown text as a string. [source](../autodoc/core/gemini_client.py)

---

## Examples

### Manual Doc Generation
While Auto-Doc usually runs via git hooks, you can use the core components programmatically:

```python
from autodoc.config import Config
from autodoc.core.doc_generator import DocGenerator

# Load configuration
config = Config.load_from_file(".autodoc/config.yaml")

# Initialize generator
generator = DocGenerator(config)

# Update a specific doc manually
generator.update_docs(
    source_files=["autodoc/core/doc_generator.py"],
    doc_target="docs/core.md",
    git_context={"message": "Refactored template logic"}
)
```

### Customizing Reasoning
You can configure the AI's "Thinking" level in the `config.yaml` passed to the `DocGenerator`:

```yaml
# config.yaml
model: "gemini-3-flash-preview"
thinking_level: "high" # Options: minimal, low, medium, high
```