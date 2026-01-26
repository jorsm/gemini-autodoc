# Auto-Doc Template Repository

This repository demonstrates a **"Self-Writing Documentation"** workflow. using Git Hooks, Python, and the Google Gemini CLI.

Whenever you commit code changes to the `src/` directory, a post-commit hook triggers a Gemini Agent to analyze the code and automatically update the documentation in `docs/API.md`.

## ✨ Features

- **Zero-Touch Logic**: No need to manually run scripts. Just `git commit`.
- **Context-Aware**: Uses your local Gemini CLI (with your API Key) to understand your code.
- **Instant Updates**: Documentation updates happen locally, immediately after the commit.

## 🚀 Setup

### 1. Prerequisites

You must have the **Gemini CLI** installed and your **API Key** configured.

```bash
# 1. Install Gemini CLI
npm install -g @google/gemini-cli
```

### Configuration

Choose one of the following methods to set your API Key:

- **Option A: Environment Variable (.env)**

  Create a `.env` file in the root of the repo:

  ```bash
  echo 'GEMINI_API_KEY="AIzaSyYourKeyHere"' > .env
  ```

- **Option B: Shell Profile**

  Add your API Key to your shell profile (e.g., `.zshrc`, `.bashrc`, `.profile`):

  ```bash
  export GEMINI_API_KEY="AIzaSyYourKeyHere"
  ```

### 2. Install the Hook

Clone this repository and run the installer script to set up the Git hooks (since hooks are not cloned by default).

```bash
git clone https://github.com/your-username/auto-doc-template.git
cd auto-doc-template

# Install the git hooks
./install_hook.sh
```

## 📖 Usage

1. **Modify Code**: Edit `src/main.py` (or any file in `src/`).

2. **Commit**:

   ```bash
   git add src/main.py
   git commit -m "feat: added new magic function"
   ```

3. **Watch Magic**:
    - The hook will run automatically.
    - You will see `🤖 Git Hook: Triggering Auto-Documentation...`.
    - `docs/API.md` will be updated with the new documentation.

4. **Finalize**:
    - Check the changes in `docs/API.md`.
    - Stage and commit the docs:

      ```bash
      git add docs/API.md
      git commit --amend --no-edit  # Or make a new commit
      ```

## 📂 Structure

- `.auto-doc/scripts/`: Contains the Python logic (`auto_doc.py`) and shell wrapper.
- `src/`: Source code directory (watched for changes).
- `docs/`: Documentation directory (auto-updated).
- `install_hook.sh`: Helper script to set up the local `.git/hooks`.

---

*Powered by Google Gemini*
