import argparse

from autodoc.config import Config
from autodoc.core.doc_generator import DocGenerator
from autodoc.utils.git_handler import GitHandler


def main():
    parser = argparse.ArgumentParser(description="Auto-Doc Agent")
    parser.add_argument("--repo", default=".", help="Path to git repo")
    args = parser.parse_args()

    # Load Config
    config = Config.load()
    # Override config with args if necessary
    config.repo_path = args.repo

    print("🤖 Auto-Doc Agent: Analyzing changes...")

    git_handler = GitHandler(config.repo_path)
    changed_files = git_handler.get_changed_files()

    # Filter for src check
    prefix = (
        config.source_dir + "/"
        if not config.source_dir.endswith("/")
        else config.source_dir
    )
    if not any(f.startswith(prefix) for f in changed_files):
        print(f"No changes in {config.source_dir}, skipping doc sync.")
        return

    print(f"Detected changes in: {changed_files}")

    generator = DocGenerator(config)
    generator.run()


if __name__ == "__main__":
    main()
