import os
import subprocess
import sys

from google import genai
from google.genai import types


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
    try:
        changed_files = run_git_command(diff_cmd).splitlines()
    except Exception:
        # Initial commit or error
        changed_files = []

    # Only run if src/ changed
    if not any(f.startswith("src/") for f in changed_files):
        print("No changes in src/, skipping doc sync.")
        return

    src_content = get_file_content("src/main.py")
    doc_content = get_file_content("docs/API.md")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    prompt = f"""
SOURCE CODE (src/main.py):
{src_content}

CURRENT DOCUMENTATION (docs/API.md):
{doc_content}
"""

    print("🤖 Auto-Doc Agent: Asking Gemini 3 (google-genai SDK) to regenerate docs...")

    try:
        client = genai.Client(api_key=api_key)

        # Define the system instruction separately
        sys_instruction = """
You are an expert technical writer. Your task is to update the documentation to match the latest source code.
1. Analyze the source code and identify all functions and exceptions.
2. Rewrite the documentation to accurately reflect the source code.
3. Ensure all parameters, return values, and raised exceptions are documented.
4. Keep the existing markdown structure.
5. The output must be the raw markdown content for the new file.
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Keep low for documentation precision
                system_instruction=sys_instruction,
                thinking_config=types.ThinkingConfig(
                    include_thoughts=False,  # We just want the doc, not the reasoning trace
                    thinking_level="High",
                ),
            ),
        )

        new_doc_content = response.text.strip()

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
        print(f"❌ Failed to run Gemini agent: {e}")


if __name__ == "__main__":
    main()
