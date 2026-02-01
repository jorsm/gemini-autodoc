# Configuration

The documentation generation process can be customized using a configuration file. By default, the system looks for configuration in the following locations (in order of priority):

1. An explicit path passed via arguments.
2. `.autodoc/config.yaml`
3. `.autodoc.yaml` (Legacy)

If no configuration file is found, the system uses default settings with no file mappings defined.

## Configuration Fields

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `repo_path` | `str` | `"."` | The root directory of the repository. |
| `source_dir` | `str` | `"src"` | (Legacy/Fallback) The directory containing source code to be documented. |
| `doc_file` | `str` | `"docs/reference.md"` | (Legacy/Fallback) The target file for generated documentation. |
| `model` | `str` | `"gemini-3-flash-preview"` | The Gemini model version to use for analysis. |
| `thinking_level` | `str` | `"high"` | The reasoning intensity for the model. |
| `prompt_template` | `str` | `None` | Optional path or string for a custom prompt. |
| `system_instruction_template` | `str` | `None` | Optional path or string for a custom system instruction. |
| `context` | `dict` | `{"files": ["README.md"]}` | Global context provided to the model for better understanding of the project. |
| `mappings` | `list` | `None` | A list of source-to-documentation mappings. |

### Advanced Context
The `context` field allows you to specify files that the Gemini Agent should read to understand the project's purpose and style before documenting specific source files. 

**Example:**
```yaml
context:
  files:
    - "README.md"
    - "CONTRIBUTING.md"
```

### Mappings
The `mappings` field is the modern way to define which source files trigger updates to specific documentation files.

**Example:**
```yaml
mappings:
  - source: "src/**"
    doc: "docs/API.md"
  - source: "internal/utils/*.py"
    doc: "docs/internals.md"
```

## Example Configuration File

Create a file at `.autodoc/config.yaml` to customize the behavior:

```yaml
# .autodoc/config.yaml
model: "gemini-3-flash-preview"
thinking_level: "high"

context:
  files:
    - "README.md"

mappings:
  - source: "src/api/*.py"
    doc: "docs/API.md"
  - source: "src/core/*.py"
    doc: "docs/CORE.md"
```

## Programmatic Usage

### `Config` Class
The `Config` class is a Python dataclass used to represent the current configuration state.

#### `Config.load(config_path: str = None) -> Config`
A class method that resolves and loads the configuration file.
- **Parameters**: `config_path` (Optional) – An explicit path to a YAML configuration file.
- **Returns**: An instance of the `Config` class.