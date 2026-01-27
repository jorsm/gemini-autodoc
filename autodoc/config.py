import os
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    repo_path: str = "."
    source_dir: str = "src"
    doc_file: str = "docs/API.md"
    model: str = "gemini-3-flash-preview"
    prompt_template: str = None  # Default handled in code

    @classmethod
    def load(cls, config_path: str = ".autodoc.yaml"):
        if not os.path.exists(config_path):
            return cls()

        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}

        return cls(
            repo_path=data.get("repo_path", "."),
            source_dir=data.get("source_dir", "src"),
            doc_file=data.get("doc_file", "docs/API.md"),
            model=data.get("model", "gemini-3-flash-preview"),
            prompt_template=data.get("prompt_template"),
        )
