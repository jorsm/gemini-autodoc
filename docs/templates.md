# Templates Documentation

This project uses Jinja2 templates to define the prompts used by the AI agent to generate and update documentation. These templates are located in the `.autodoc/templates/` directory.

## Documentation Prompt (`doc_prompt.j2`)

The `doc_prompt.j2` file is the primary template used to instruct the Gemini model on how to analyze code changes and update the corresponding documentation files. It structures the prompt to provide the AI with both local code changes and global project context.

### Available Variables

When the template is rendered by the auto-doc logic, the following variables are provided:

| Variable | Type | Description |
| :--- | :--- | :--- |
| `sources` | `List[Dict]` | A list of source code files that triggered the update. Each dictionary contains `path` (str) and `content` (str). |
| `context_files` | `List[Dict]` | A list of global context files defined in the project configuration. Each dictionary contains `path` (str) and `content` (str). |
| `doc_file` | `str` | The file path of the documentation file currently being updated (e.g., `docs/API.md`). |
| `doc_content` | `str` | The existing text content of the documentation file before the current update process. |

### Template Structure

The template is organized into specific sections to help the AI model distinguish between background information and the code it needs to document:

1.  **GLOBAL CONTEXT**: Iterates through `context_files` to provide the AI with high-level project information (e.g., the `README.md`).
2.  **SOURCE CODE (Changed Files)**: Iterates through `sources` to present the actual code logic, classes, and functions that have been modified.
3.  **CURRENT DOCUMENTATION**: Provides the current content of the `doc_file` so the AI can perform an incremental update rather than a full rewrite.
4.  **INSTRUCTIONS**: Explicit directives for the AI to ensure it reflects the source code changes accurately and returns only the raw Markdown content.