# Trigger Doc Update
from pathlib import Path

from jinja2 import Template

from autodoc.config import Config
from autodoc.core.gemini_client import GeminiClient
from autodoc.utils.logger import setup_logger

logger = setup_logger()


class DocGenerator:
    def __init__(self, config: Config):
        self.config = config
        try:
            self.client = GeminiClient(model=config.model)
        except ValueError as e:
            logger.warning(f"⚠️  {e}")
            self.client = None

    def update_docs(self, source_files: list, doc_target: str):
        if not self.client:
            logger.error("Skipping Auto-Doc: Client not initialized (missing API Key?)")
            return

        # 1. Read Source Files
        sources = []
        for src_file in source_files:
            path = Path(src_file)
            if path.exists():
                sources.append(
                    {"path": str(path), "content": path.read_text(encoding="utf-8")}
                )

        if not sources:
            logger.warning(f"No valid source files found in: {source_files}")
            return

        # 2. Read Global Context
        context_files = []
        if self.config.context and self.config.context.get("files"):
            for ctx_file in self.config.context["files"]:
                path = Path(ctx_file)
                if path.exists():
                    context_files.append(
                        {"path": str(path), "content": path.read_text(encoding="utf-8")}
                    )

        # 3. Read Target Doc
        doc_path = Path(doc_target)
        doc_content = ""
        if doc_path.exists():
            doc_content = doc_path.read_text(encoding="utf-8")

        # 4. Build Prompt
        prompt = self._render_prompt(sources, context_files, str(doc_path), doc_content)

        system_instruction = """
You are an expert technical writer. Your task is to update the documentation to match the latest source code.
1. Analyze the source code and global context.
2. Rewrite or update the target documentation to accurately reflect the source code.
3. Keep the existing markdown structure unless a refactor is clearly needed.
4. The output must be the raw markdown content for the new file.
"""

        logger.info(
            f"🤖 Auto-Doc: Updating {doc_target} using {len(sources)} source files..."
        )
        try:
            new_doc = self.client.generate_documentation(
                prompt, system_instruction, thinking_level=self.config.thinking_level
            )
        except Exception as e:
            logger.error(f"❌ Failed to generate docs: {e}")
            return

        # 5. Clean and Write
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

        logger.info(f"✅ Updated {doc_target}")

    def _render_prompt(self, sources, context_files, doc_path, doc_content):
        template_str = ""
        # Check config custom template
        if self.config.prompt_template and Path(self.config.prompt_template).exists():
            template_str = Path(self.config.prompt_template).read_text(encoding="utf-8")
        else:
            # Fallback to internal default
            default_tpl = Path("autodoc/templates/default_prompt.j2")
            if default_tpl.exists():
                template_str = default_tpl.read_text(encoding="utf-8")
            else:
                # Basic Fallback
                template_str = """
GLOBAL CONTEXT:
{% for ctx in context_files %}
-- {{ ctx.path }} --
{{ ctx.content }}
{% endfor %}

SOURCE CODE:
{% for src in sources %}
-- {{ src.path }} --
{{ src.content }}
{% endfor %}

CURRENT DOCUMENTATION ({{ doc_file }}):
{{ doc_content }}
"""

        t = Template(template_str)
        return t.render(
            sources=sources,
            context_files=context_files,
            doc_file=doc_path,
            doc_content=doc_content,
        )
