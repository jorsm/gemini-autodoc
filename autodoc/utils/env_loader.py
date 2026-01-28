import os


def load_env(paths=None):
    """
    Manually load environment variables from .env files.
    Checks paths in order. Defaults to [".env", ".autodoc/.env"].
    Does not override existing environment variables.
    """
    if paths is None:
        paths = [".env", ".autodoc/.env"]

    # Ensure it's iterable
    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        if not os.path.exists(path):
            continue

        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Unwrap quotes if present
                    if (value.startswith('"') and value.endswith('"')) or (
                        value.startswith("'") and value.endswith("'")
                    ):
                        value = value[1:-1]

                    # Only set if not already set (respect system envs)
                    if key and key not in os.environ:
                        os.environ[key] = value
