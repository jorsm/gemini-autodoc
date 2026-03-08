from collections import defaultdict

import pathspec

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
    git_context = git_handler.get_commit_context()

    if not changed_files:
        logger.info("No changes detected.")
        return

    logger.info(f"Detected changes in: {changed_files}")

    # Router Logic
    # Map target_doc -> [list of source files]
    doc_updates = defaultdict(list)

    if config.mappings:
        for changed_file in changed_files:
            # changed_file is relative to repo root (e.g. "src/main.py")

            for mapping in config.mappings:
                source_glob = mapping.get("source")
                target_doc = mapping.get("doc")

                # Parse the source glob as a git pathspec wildcard
                spec = pathspec.PathSpec.from_lines("gitwildmatch", [source_glob])

                if spec.match_file(changed_file):
                    # CHECK EXCLUSIONS
                    excludes = mapping.get("exclude", [])
                    is_excluded = False

                    if excludes:
                        exc_spec = pathspec.PathSpec.from_lines(
                            "gitwildmatch", excludes
                        )
                        is_excluded = exc_spec.match_file(changed_file)

                    if is_excluded:
                        continue

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
        generator.update_docs(sources, doc_target, git_context=git_context)
# trigger autodoc
# trigger autodoc
# rel links
# force link rewrite
# local templates

# force update docs
