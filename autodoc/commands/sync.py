from autodoc.config import Config
from autodoc.core.doc_generator import DocGenerator
from autodoc.utils.git_handler import GitHandler
from autodoc.utils.logger import setup_logger

logger = setup_logger()


def sync_docs(repo_path: str = "."):
    """
    Analyzes changes and syncs documentation.
    """
    logger.info("Starting documentation sync...")

    # Load Config
    config = Config.load()
    if repo_path != ".":
        config.repo_path = repo_path

    git_handler = GitHandler(config.repo_path)
    changed_files = git_handler.get_changed_files()

    logger.info(f"Changed files detected: {changed_files}")

    # Calculate prefix for basic filtering "src/"
    prefix = (
        config.source_dir + "/"
        if not config.source_dir.endswith("/")
        else config.source_dir
    )

    # Identify relevant files
    relevant_files = [f for f in changed_files if f.startswith(prefix)]

    if not relevant_files:
        logger.info(f"No changes in {config.source_dir}, skipping doc sync.")
        return

    logger.info(f"Processing relevant files: {relevant_files}")

    # TODO: In future, pass relevant_files to run() for granular updates
    # For now, we stick to the main.py logic but log the intent.
    generator = DocGenerator(config)
    generator.run()
