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
                if diff.change_type in ["A", "M", "R"] and diff.b_path:
                    files.append(diff.b_path)
        except Exception as e:
            print(f"Git error: {e}")
            return []

        return files

    def get_commit_context(self, commit: str = "HEAD") -> dict:
        """
        Get metadata about a specific commit.
        """
        if not self.repo:
            return {}

        try:
            c = self.repo.commit(commit)
            return {
                "hash": c.hexsha,
                "message": c.message.strip(),
                "author": c.author.name,
                "author_email": c.author.email,
                "date": c.committed_datetime.isoformat(),
            }
        except (git.exc.BadName, ValueError, Exception) as e:
            print(f"Git error getting commit context: {e}")
            return {}

    def get_root_dir(self) -> str:
        if self.repo:
            return self.repo.working_dir
        return os.getcwd()
# trigger autodoc
# trigger autodoc
# rel links
# force link rewrite
# local templates
