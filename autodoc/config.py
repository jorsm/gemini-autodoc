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
    prompt_template: Optional[str] = None

    # New Fields
    context: Optional[Dict] = None  # e.g. {"files": ["README.md"]}
    mappings: Optional[List] = None  # e.g. [{"source": "src/**", "doc": "docs/API.md"}]

    @classmethod
    def load(cls, config_path: str = ".autodoc.yaml"):
        # Default Config (Legacy Mode)
        default_config = {
            "source_dir": "src",
            "doc_file": "docs/API.md",
            "model": "gemini-3-flash-preview",
            "context": {"files": ["README.md"]},
            "mappings": [],
        }

        # Check legacy default config location (repo root)
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                default_config.update(data)
        elif os.path.exists(".autodoc/config.yaml"):
            with open(".autodoc/config.yaml", "r") as f:
                data = yaml.safe_load(f) or {}
                default_config.update(data)

        # Backwards compatibility: If no mappings defined, create one from source_dir/doc_file
        if not default_config.get("mappings"):
            default_config["mappings"] = [
                {
                    "name": "Default",
                    "source": f"{default_config['source_dir']}/**/*.py",
                    "doc": default_config["doc_file"],
                }
            ]

        return cls(
            repo_path=default_config.get("repo_path", "."),
            source_dir=default_config.get("source_dir"),
            doc_file=default_config.get("doc_file"),
            model=default_config.get("model"),
            prompt_template=default_config.get("prompt_template"),
            context=default_config.get("context"),
            mappings=default_config.get("mappings"),
        )
