# Auto-Doc Agent

![Auto-Doc Status](https://img.shields.io/badge/status-active-success.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Gemini Model](https://img.shields.io/badge/model-Gemini%203%20Flash%2FPro-orange)

**Never write stale documentation again.**

Auto-Doc is an intelligent AI agent that lives in your git repository. It watches your commits, analyzes your code changes using **Google's Gemini 3 (Thinking Models)**, and automatically updates your documentation to match the new reality of your codebase.

---

## 📋 Table of Contents

- [Auto-Doc Agent](#auto-doc-agent)
  - [📋 Table of Contents](#-table-of-contents)
  - [🚀 Key Features](#-key-features)
  - [📦 Installation](#-installation)
    - [Option A: Install from GitHub (Recommended)](#option-a-install-from-github-recommended)
    - [Option B: Local Development](#option-b-local-development)
    - [Authentication](#authentication)
  - [⚡ Quick Start](#-quick-start)
  - [⚙️ Configuration](#️-configuration)
  - [📂 Project Structure \& Documentation](#-project-structure--documentation)
  - [🛠️ Contributing](#️-contributing)

---

## 🚀 Key Features

- **🤖 Zero-Click Updates**: Runs automatically via a standard Git Post-Commit Hook. You code, it documents.
- **🧠 Deep Reasoning**: Leverages Gemini 3.0's "Thinking" capabilities to understand complex logic changes, not just syntax.
- **📚 Context Awareness**: Define "Global Context" files (like `README.md` or `ARCHITECTURE.md`) that are always included in the prompt, ensuring the AI understands the bigger picture.
- **🗺️ Config-Driven Routing**: Precisely map source files (globs) to specific documentation files (e.g., `src/core/*.py` → `docs/core.md`). **Matches are evaluated top-to-bottom (Priority Rule)**.
- **🎨 Custom Templates**: Full control over the AI's output using Jinja2 templates.
- **🖥️ IDE Compatible**: Works with **VS Code** or any Git client that triggers hooks.
- **🐕 Dogfooding**: This project documents itself using Auto-Doc!

## 📦 Installation

You can install Auto-Doc directly from the repository using `pip`.

### Option A: Install from GitHub (Recommended)
Add to your `requirements.txt`:
```text
git+https://github.com/jorsm/gemini-autodoc.git@main
```
Or install via command line:
```bash
pip install git+https://github.com/jorsm/gemini-autodoc.git
```

### Option B: Local Development
Cloning the source is useful if you want to modify the agent itself.
```bash
git clone https://github.com/jorsm/gemini-autodoc.git
cd auto-doc
pip install -e .
```

### Authentication
Auto-Doc requires a Google Gemini API Key.
1.  **Environment Variable** (Best for CI/CD):
    ```bash
    export GEMINI_API_KEY="your-api-key-here"
    ```
2.  **.env File**:
    Create a file named `.env` in your project root or inside `.autodoc/.env`. Auto-Doc expects ONE line:
    ```bash
    GEMINI_API_KEY=your-api-key-here
    ```

## ⚡ Quick Start

1.  **Initialize Auto-Doc**:
    Run inside your project root. This creates `.autodoc/` and installs the git hook.
    ```bash
    autodoc init
    ```

2.  **Configure Mappings**:
    Edit `.autodoc/config.yaml` to define which code updates which docs.
    *   See the deeply detailed [Configuration Reference](docs/configuration.md) for full options.

    A basic configuration tells Auto-Doc three things:
    - **Context**: Which global files (like `README.md`) the AI should always read.
    - **Mappings**: A priority ordered list Mapping Python source paths (like `src/**/*.py`) to Markdown Target paths (like `docs/api.md`).
    - **Model Settings**: Which Gemini version and "Thinking" depth to use.

3.  **Code & Commit**:
    ```bash
    git add .
    git commit -m "feat: implemented user login"
    ```
    
    > **Note**: This works automatically in **VS Code**, JetBrains, or the terminal. 
    > The AI hook runs in the background, analyzing changes and generating documentation.

## ⚙️ Configuration

Auto-Doc is highly configurable via `.autodoc/config.yaml`. The schema is documented directly by the tool itself:

| Feature | Description | Reference |
| :--- | :--- | :--- |
| **Mappings & Glob Matching** | How to map source code to doc files. | [Configuration Docs](docs/configuration.md) |
| **Model Optimization** | Control Gemini's reasoning depth. | [Configuration Docs](docs/configuration.md) |

## 📂 Project Structure & Documentation

This project's documentation is **automatically generated** from its source code by Auto-Doc. Explore the `docs/` folder to see the direct results:

- **[Core Logic](docs/core.md)**: The internal `DocGenerator` engine and `GeminiClient`.
- **[CLI Commands](docs/commands.md)**: The `init` and sync workflows.
- **[Configuration](docs/configuration.md)**: Details on the `Config` schema.
- **[Utilities](docs/utils.md)**: Git helpers and logging.

## 🛠️ Contributing

1.  Fork the repo.
2.  Create a feature branch.
3.  Commit your changes (Auto-Doc will try to document them!).
4.  Push and open a PR.

---
*Powered by Google Gemini*
