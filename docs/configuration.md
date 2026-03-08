# Configuration

The Configuration module handles the loading and parsing of project-specific settings for Auto-Doc. It defines how the AI behaves, which files it monitors, and how it maps source changes to documentation updates.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
    - [Config Dataclass](#config-dataclass)
    - [Config.load()](#configload)
- [Configuration Schema](#configuration-schema)

---

## Core Concepts

Auto-Doc uses a YAML-based configuration file (typically `.autodoc/config.yaml`). The configuration is loaded into a strictly typed `Config` dataclass.

**Resolution Priority:**
When looking for a configuration file, the system follows this order:
1.  **Explicit Path**: A path passed directly to the `load()` method.
2.  **Standard Path**: `.autodoc/config.yaml` in the project root.
3.  **Legacy Path**: `.autodoc.yaml` in the project root.
4.  **Default Instance**: If no file is found, a default configuration is returned with empty mappings.

---

## API Reference

### Config Dataclass
The primary container for all application settings.

| Field | Type | Default (via `load`) | Description |
| :--- | :--- | :--- | :--- |
| `repo_path` | `str` | `"."` | The absolute or relative path to the git repository. |
| `doc_file` | `str` | `"docs/reference.md"` | Default target documentation file used if no specific mapping matches. |
| `model` | `str` | `"gemini-3-flash-preview"` | The specific Google Gemini model to use. |
| `thinking_level` | `str` | `"high"` | Controls the reasoning depth of the model. |
| `prompt_template` | `Optional[str]` | `None` | Custom path or string for the Jinja2 user prompt template. |
| `system_instruction_template` | `Optional[str]` | `None` | Custom path or string for the AI system instructions. |
| `context` | `Optional[Dict]` | `{"files": ["README.md"]}` | Global context settings, typically a list of files always sent to the AI. |
| `mappings` | `Optional[List]` | `None` | A list of rules mapping source file patterns (globs) to documentation files. |

[source](../autodoc/config.py)

### Config.load()
`@classmethod load(config_path: str = None) -> Config`

Loads the configuration from a YAML file. If no path is provided, it searches the default locations mentioned in [Core Concepts](#core-concepts). If no configuration file is found anywhere, it returns a minimal `Config` instance with an empty mapping list.

**Parameters:**
- `config_path`: Optional explicit path to a `.yaml` configuration file.

**Returns:**
- An initialized `Config` instance populated with YAML values or sensible defaults.

[source](../autodoc/config.py)

---

## Configuration Schema

The YAML file structure expected by Auto-Doc:

```yaml
# .autodoc/config.yaml

# The AI Model settings
model: "gemini-3-flash-preview"
thinking_level: "high"

# Global context included in every AI request
context:
  files:
    - "README.md"
    - "ARCHITECTURE.md"

# Priority-based routing (Top-to-bottom)
mappings:
  - source: "autodoc/*.py"
    doc: "docs/core.md"
    
  - source: "autodoc/utils/*.py"
    doc: "docs/utils.md"

# Optional: Override templates
# prompt_template: "templates/custom_prompt.j2"
# system_instruction_template: "templates/custom_system.j2"
```

### Mapping Rules
Mappings are evaluated in order (**Priority Rule**). The first rule that matches a changed file (using glob patterns) determines which documentation file will be updated. This allows you to create specific documentation for subdirectories or modules while having a "catch-all" pattern at the bottom of the list.