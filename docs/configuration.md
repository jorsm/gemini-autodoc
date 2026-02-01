# Configuration

The documentation generation process is controlled by a configuration file. By default, the system searches for configuration in the following order of priority:

1.  An explicit path passed via the `--config` argument.
2.  `.autodoc/config.yaml`
3.  `.autodoc.yaml` (Legacy)

If no configuration file is found, the system uses internal defaults.

## Configuration Fields

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `repo_path` | `str` | `"."` | The root directory of the repository. |
| `model` | `str` | `"gemini-3-flash-preview"` | The Gemini model version used for code analysis. |
| `thinking_level` | `str` | `"high"` | The reasoning intensity for the model. |
| `prompt_template` | `str` | `None` | Path to a custom Jinja2 template for the model prompt. |
| `system_instruction_template` | `str` | `None` | Path to a custom Jinja2 template for the system instructions. |
| `context` | `dict` | `{"files": ["README.md"]}` | Global files provided to the model to establish project-wide context. |
| `mappings` | `list` | `None` | A list of source-to-documentation mapping objects. |

### Global Context
The `context` field allows you to specify files that the Gemini Agent should ingest to understand the project's architecture, naming conventions, and style before it documents specific source files.

**Example:**
```yaml
context:
  files:
    - "README.md"
    - "CONTRIBUTING.md"
```

### Mappings
The `mappings` field defines which source files are analyzed and which documentation files they update. Each mapping entry supports the following properties:

*   `name`: (Optional) A descriptive label for the mapping.
*   `source`: A glob pattern matching the source files to watch.
*   `doc`: The target Markdown file to be updated.

**Example:**
```yaml
mappings:
  - name: "Core Logic"
    source: "src/core/*.py"
    doc: "docs/core.md"
  - name: "API Layer"
    source: "src/api/**/*.py"
    doc: "docs/api_reference.md"
```

## Example Configuration File

This is a representative `.autodoc/config.yaml` showing how to map different modules to specific documentation files:

```yaml
# .autodoc/config.yaml

# Global Context
context:
  files:
    - "README.md"

# Mappings
mappings:
  - name: "Core Modules"
    source: "autodoc/core/*.py"
    doc: "docs/core.md"

  - name: "CLI Commands"
    source: "autodoc/commands/*.py"
    doc: "docs/commands.md"

  - name: "Configuration"
    source: "autodoc/config.py"
    doc: "docs/configuration.md"

# Templates
prompt_template: ".autodoc/templates/doc_prompt.j2"
system_instruction_template: ".autodoc/templates/system_instruction.j2"

# Model Settings
model: "gemini-3-flash-preview"
thinking_level: "high"
```

## Programmatic Usage

### `Config` Class
The `Config` class is a Python dataclass that represents the configuration state.

#### `Config.load(config_path: str = None) -> Config`
A class method that resolves and loads the configuration file into a `Config` object.
- **Parameters**: `config_path` (Optional) – An explicit path to a YAML configuration file.
- **Returns**: An instance of the `Config` class populated with file or default values.