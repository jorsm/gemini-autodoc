---
description: Sync documentation with staged changes in src/
---

# Documentation Sync

Sync documentation with staged changes in `src/`.

## Steps

1. **Check for Staged Changes**: Verify if any files in `src/` are currently staged.

   ```bash
   git diff --cached --name-only src/
   ```

2. **Execute Documentation Sync Skill**:
   - Compare staged changes against the last commit.
   - Identify logic changes, function signature updates, or new configurations.
   - Update relevant files in `docs/` or `README.md`.

3. **Generate Artifact**: Present the proposed changes as a reviewable diff artifact.

4. **Wait for Confirmation**: Ask the user to review and confirm the changes.

5. **Stage Updates**: Once confirmed, add the updated documentation to the git stage.
