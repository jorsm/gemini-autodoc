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

        sources = self._read_files_with_content(source_files)
        if not sources:
            logger.warning(f"No valid source files found in: {source_files}")
            return

        context_paths = []
        if self.config.context and self.config.context.get("files"):
            context_paths = self.config.context["files"]
        context_files = self._read_files_with_content(context_paths)

        doc_path = Path(doc_target)
        doc_content = doc_path.read_text(encoding="utf-8") if doc_path.exists() else ""

        prompt = self._render_template(
            self.config.prompt_template,
            "autodoc/templates/default_prompt.j2",
            sources=sources,
            context_files=context_files,
            doc_file=doc_path,
            doc_content=doc_content,
        )

        system_instruction = self._render_template(
            self.config.system_instruction_template,
            "autodoc/templates/system_instruction.j2",
        )

        if not system_instruction:
            system_instruction = "You are an expert technical writer. Update the documentation to match the source code."

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

        new_doc = self._clean_markdown_response(new_doc)

        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(new_doc, encoding="utf-8")

        logger.info(f"✅ Updated {doc_target}")

    def _read_files_with_content(self, file_paths: list) -> list:
        results = []
        for f in file_paths:
            path = Path(f)
            if path.exists():
                results.append(
                    {"path": str(path), "content": path.read_text(encoding="utf-8")}
                )
        return results

    def _clean_markdown_response(self, text: str) -> str:
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            return "\n".join(lines)
        return text

    def _render_template(self, config_path, default_path, **kwargs):
        """
        Loads and renders a Jinja2 template.
        Priority: 1. Configured Path, 2. Default Internal Path.
        """
        template_str = ""

        # 1. Try Configured Path
        if config_path:
            p = Path(config_path)
            if p.exists():
                template_str = p.read_text(encoding="utf-8")

        # 2. Try Default Internal Path (if configured path missing or not set)
        if not template_str:
            p = Path(default_path)
            if p.exists():
                template_str = p.read_text(encoding="utf-8")

        if not template_str:
            logger.warning(f"⚠️  Template not found: {config_path} or {default_path}")
            return ""

        t = Template(template_str)
        return t.render(**kwargs)
