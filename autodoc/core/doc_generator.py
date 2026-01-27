from pathlib import Path

from jinja2 import Template

from autodoc.config import Config
from autodoc.core.gemini_client import GeminiClient


class DocGenerator:
    def __init__(self, config: Config):
        self.config = config
        try:
            self.client = GeminiClient(model=config.model)
        except ValueError as e:
            print(f"⚠️  {e}")
            self.client = None

    def run(self):
        if not self.client:
            print("Skipping Auto-Doc: Client not initialized (missing API Key?)")
            return

        # 1. Read Source
        src_path = Path(self.config.source_dir) / "main.py"
        if not src_path.exists():
            print(f"Source file {src_path} not found.")
            return

        src_content = src_path.read_text(encoding="utf-8")

        # 2. Read Doc
        doc_path = Path(self.config.doc_file)
        doc_content = ""
        if doc_path.exists():
            doc_content = doc_path.read_text(encoding="utf-8")

        # 3. Build Prompt
        prompt = self._render_prompt(str(src_path), src_content, doc_content)

        system_instruction = """
You are an expert technical writer. Your task is to update the documentation to match the latest source code.
1. Analyze the source code and identify all functions and exceptions.
2. Rewrite the documentation to accurately reflect the source code.
3. Ensure all parameters, return values, and raised exceptions are documented.
4. Keep the existing markdown structure.
5. The output must be the raw markdown content for the new file.
"""

        print(f"🤖 Auto-Doc Agent: Asking {self.config.model} to regenerate docs...")
        try:
            new_doc = self.client.generate_documentation(prompt, system_instruction)
        except Exception:
            print("❌ Failed to generate docs.")
            return

        # 4. Clean and Write
        if new_doc.startswith("```"):
            lines = new_doc.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            new_doc = "\n".join(lines)

        # Ensure parent dirs exist
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(new_doc, encoding="utf-8")

        print(f"✅ Auto-Doc Agent: Updated {self.config.doc_file}")

    def _render_prompt(self, src_path, src_content, doc_content):
        template_str = ""
        # Check config custom template
        if self.config.prompt_template and Path(self.config.prompt_template).exists():
            template_str = Path(self.config.prompt_template).read_text(encoding="utf-8")
        else:
            # Fallback to internal default
            # Assuming running from repo root
            default_tpl = Path("autodoc/templates/default_prompt.j2")
            if default_tpl.exists():
                template_str = default_tpl.read_text(encoding="utf-8")
            else:
                template_str = """
SOURCE CODE ({{ src_path }}):
{{ src_content }}

CURRENT DOCUMENTATION ({{ doc_file }}):
{{ doc_content }}
"""

        t = Template(template_str)
        return t.render(
            src_path=src_path,
            src_content=src_content,
            doc_file=self.config.doc_file,
            doc_content=doc_content,
        )
