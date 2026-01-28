import argparse

from autodoc.commands.init import init_project
from autodoc.commands.sync import sync_docs


def main():
    parser = argparse.ArgumentParser(description="Auto-Doc Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init Command
    subparsers.add_parser("init", help="Install git hooks")

    # Sync Command
    sync_parser = subparsers.add_parser("sync", help="Run documentation sync")
    sync_parser.add_argument("--repo", default=".", help="Path to git repo")

    args = parser.parse_args()

    if args.command == "init":
        init_project()
    elif args.command == "sync":
        sync_docs(repo_path=args.repo)


if __name__ == "__main__":
    main()
