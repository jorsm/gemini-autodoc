from collections import defaultdict
from pathlib import Path

from autodoc.config import Config
from autodoc.core.doc_generator import DocGenerator
from autodoc.utils.git_handler import GitHandler
from autodoc.utils.logger import setup_logger

logger = setup_logger()


def sync_docs(repo_path="."):
    # Load Config
    # If called from CLI, we might want to respect CWD or repo_path
    # Config.load determines path automatically.
    config = Config.load()
    config.repo_path = repo_path

    logger.info("🤖 Auto-Doc: Analyzing changes...")

    git_handler = GitHandler(config.repo_path)
    changed_files = git_handler.get_changed_files()

    if not changed_files:
        logger.info("No changes detected.")
        return

    logger.info(f"Detected changes in: {changed_files}")

    # Router Logic
    # Map target_doc -> [list of source files]
    doc_updates = defaultdict(list)

    if config.mappings:
        repo_root = Path(config.repo_path).resolve()

        for changed_file in changed_files:
            # changed_file is relative to repo root (e.g. "src/main.py")
            # Create full path for matching
            full_file_path = repo_root / changed_file

            for mapping in config.mappings:
                source_glob = mapping.get("source")
                target_doc = mapping.get("doc")

                # Construct absolute glob pattern
                # We assume source_glob is relative to repo root
                abs_glob = f"{repo_root}/{source_glob}"

                # Use Path.match on the full path
                if full_file_path.match(abs_glob):
                    doc_updates[target_doc].append(changed_file)
                    # Stop at first match (Priority Rule)
                    break

    if not doc_updates:
        logger.info(
            "No relevant source (src/) changes detected based on config mappings."
        )
        return

    # Execute Updates
    generator = DocGenerator(config)
    for doc_target, sources in doc_updates.items():
        logger.info(f"Triggering update for {doc_target} with sources: {sources}")
        generator.update_docs(sources, doc_target)
# Trigger Update
