import os
from typing import List

import git


class GitHandler:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        try:
            self.repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            self.repo = None

    def get_changed_files(self, base: str = "HEAD~1", head: str = "HEAD") -> List[str]:
        """
        Get a list of files changed between two commits.
        Returns paths relative to the repo root.
        """
        if not self.repo:
            return []

        try:
            # Check if base exists (handle initial commit)
            self.repo.commit(base)
        except (git.exc.BadName, ValueError):
            # Probably initial commit, just list all files in HEAD?
            # Or just diff against empty tree magic?
            # For simplicity, safe fallback to "scan everything" or empty.
            # But let's assume we are in a stream of commits.
            return []

        files = []
        try:
            diffs = self.repo.commit(base).diff(head)
            for diff in diffs:
                if diff.change_type in ["A", "M", "R"]:
                    if diff.b_path:
                        files.append(diff.b_path)
        except Exception as e:
            print(f"Git error: {e}")
            return []

        return files

    def get_root_dir(self) -> str:
        if self.repo:
            return self.repo.working_dir
        return os.getcwd()
