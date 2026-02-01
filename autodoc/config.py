import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml


@dataclass
class Config:
    repo_path: str = "."
    # Legacy / Default fallback
    source_dir: str = "src"
    doc_file: str = "docs/API.md"

    model: str = "gemini-3-flash-preview"
    thinking_level: str = "high"
    prompt_template: Optional[str] = None
    system_instruction_template: Optional[str] = None

    # New Fields
    context: Optional[Dict] = None  # e.g. {"files": ["README.md"]}
    mappings: Optional[List] = None  # e.g. [{"source": "src/**", "doc": "docs/API.md"}]

    @classmethod
    def load(cls, config_path: str = None):
        # 1. Determine Config Path
        # Priority: explicit arg -> .autodoc/config.yaml -> .autodoc.yaml (legacy)
        if config_path and os.path.exists(config_path):
            final_path = config_path
        elif os.path.exists(".autodoc/config.yaml"):
            final_path = ".autodoc/config.yaml"
        elif os.path.exists(".autodoc.yaml"):
            final_path = ".autodoc.yaml"
        else:
            # Fallback for fresh install case (before init) or minimal usage
            return cls(mappings=[])

        # 2. Load YAML
        with open(final_path, "r") as f:
            data = yaml.safe_load(f) or {}

        # 3. Parse Fields
        return cls(
            repo_path=data.get("repo_path", "."),
            # Legacy fallback if source_dir present but mappings not
            source_dir=data.get("source_dir", "src"),
            doc_file=data.get("doc_file", "docs/reference.md"),
            model=data.get("model", "gemini-3-flash-preview"),
            thinking_level=data.get("thinking_level", "high"),
            prompt_template=data.get("prompt_template"),
            system_instruction_template=data.get("system_instruction_template"),
            context=data.get("context", {"files": ["README.md"]}),
            mappings=data.get("mappings"),
        )
