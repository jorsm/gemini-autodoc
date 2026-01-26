#!/bin/bash
# Wrapper to ensure environment variables are loaded before running the python script

# Source the user's zshrc to get the GEMINI_API_KEY
# We use zsh -c to verify variable loading if sourcing fails in sh
if [ -z "$GEMINI_API_KEY" ]; then
    # Try to extract it manually if not present
    export GEMINI_API_KEY=$(grep "export GEMINI_API_KEY" $HOME/.zshrc | cut -d '"' -f 2)
fi

# Run the python script
python3 .agent/scripts/auto_doc.py
