import os
import sys

from dotenv import load_dotenv

from autodoc.commands.sync import sync_docs
from autodoc.utils.logger import setup_logger

# Try loading .env from current directory
load_dotenv()

logger = setup_logger()


def get_api_key():
    # 1. Check Standard Env Vars (GEMINI_API_KEY, GOOGLE_API_KEY)
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key

    # 2. Add more fallbacks here if needed specifically for this tool
    return None


def main():
    logger.info("🤖 Auto-Doc Hook Triggered")

    api_key = get_api_key()
    if not api_key:
        logger.warning(
            "⚠️  API Key not found in Environment (GEMINI_API_KEY or GOOGLE_API_KEY)."
        )
        logger.warning("Please create a .env file or ensure the variable is exported.")
        logger.warning("If using a GUI Git Client, you MUST use a .env file.")
        # We exit gracefully to not block the commit
        sys.exit(0)

    # Set it back to env for the details that might rely on it implicitly
    os.environ["GEMINI_API_KEY"] = api_key

    try:
        sync_docs()
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        # Don't block commit
        sys.exit(0)


if __name__ == "__main__":
    main()
