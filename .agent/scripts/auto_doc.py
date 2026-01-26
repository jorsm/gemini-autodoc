import os
import subprocess
import sys


def run_git_command(command):
    return subprocess.check_output(command, shell=True).decode("utf-8")


def get_file_content(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def main():
    print("🤖 Auto-Doc Agent: Analyzing changes...")

    # Get the diff to see if relevant files changed
    diff_cmd = "git diff HEAD~1 HEAD --name-only"
    changed_files = run_git_command(diff_cmd).splitlines()

    # Only run if src/ changed
    if not any(f.startswith("src/") for f in changed_files):
        print("No changes in src/, skipping doc sync.")
        return

    src_content = get_file_content("src/main.py")
    doc_content = get_file_content("docs/API.md")

    prompt = f"""
You are an expert technical writer. Your task is to update the documentation to match the latest source code.

SOURCE CODE (src/main.py):
{src_content}

CURRENT DOCUMENTATION (docs/API.md):
{doc_content}

INSTRUCTIONS:
1. Analyze the source code and identify all functions and exceptions.
2. Rewrite the documentation to accurately reflect the source code.
3. Ensure all parameters, return values, and raised exceptions are documented.
4. Keep the existing markdown structure.
5. output ONLY the raw markdown content for the new file. Do not include markdown code fences (```markdown) or conversational text.
"""

    print("🤖 Auto-Doc Agent: Asking Gemini to regenerate docs...")

    # Call Gemini CLI via subprocess with the prompt passed to stdin
    # We use --no-stream (if available) or just capture stdout
    # Based on testing, default behavior is fine, but we might trap 'markdown' fences if the model adds them.

    try:
        process = subprocess.Popen(
            ["gemini"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(input=prompt)

        if process.returncode != 0:
            print(f"Error calling Gemini: {stderr}")
            return

        new_doc_content = stdout.strip()

        # Clean up potential markdown fences if the model added them
        if new_doc_content.startswith("```"):
            lines = new_doc_content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            new_doc_content = "\n".join(lines)

        # Write the update
        with open("docs/API.md", "w") as f:
            f.write(new_doc_content)

        print("✅ Auto-Doc Agent: Updated docs/API.md")

    except Exception as e:
        print(f"Failed to run Gemini agent: {e}")


if __name__ == "__main__":
    main()
