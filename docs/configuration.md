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

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `repo_path` | `str` | `""` | The absolute or relative path to the git repository. |
| `doc_file` | `str` | `""` | Default target documentation file (Legacy/Fallback). |
| `model` | `str` | `"gemini-3-flash-preview"` | The specific Google Gemini model to use. |
| `thinking_level` | `str` | `"high"` | Controls the reasoning depth of the model. |
| `prompt_template` | `Optional[str]` | `None` | Custom Jinja2 template for the user prompt. |
| `system_instruction_template` | `Optional[str]` | `None` | Custom Jinja2 template for the system instructions. |
| `context` | `Optional[Dict]` | `None` | Global context settings (e.g., `{"files": ["README.md"]}`). |
| `mappings` | `Optional[List]` | `None` | List of rules mapping source globs to documentation files. |

[source](../autodoc/config.py)

### Config.load()
`@classmethod load(config_path: str = None) -> Config`

Loads the configuration from a YAML file. If no path is provided, it searches the default locations mentioned in [Core Concepts](#core-concepts).

**Parameters:**
- `config_path`: Optional explicit path to a `.yaml` configuration file.

**Returns:**
- An initialized `Config` instance.

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
  - name: "Core Logic"
    source: "autodoc/*.py"
    target: "docs/core.md"
    exclude: ["autodoc/tests/**"]
    
  - name: "Utilities"
    source: "autodoc/utils/*.py"
    target: "docs/utils.md"

# Optional: Override templates
# prompt_template: "path/to/my_template.j2"
```

### Mapping Rules
Mappings are evaluated in order. The first rule that matches a changed file will determine which documentation file is updated. This allows you to create specific documentation for subdirectories while having a "catch-all" at the bottom.