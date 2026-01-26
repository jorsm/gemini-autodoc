#!/bin/bash
# Wrapper to ensure environment variables are loaded before running the python script

# 1. Try loading from a local .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 2. If not set, try to find it in common shell configuration files
if [ -z "$GEMINI_API_KEY" ]; then
    CONFIG_FILES=("$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile")
    
    for file in "${CONFIG_FILES[@]}"; do
        if [ -f "$file" ]; then
            # Try to grab the export line. 
            # This grep looks for 'export GEMINI_API_KEY="VAL"' or 'export GEMINI_API_KEY=VAL'
            KEY_IN_FILE=$(grep "export GEMINI_API_KEY" "$file" | head -n 1)
            
            if [ -n "$KEY_IN_FILE" ]; then
                # Clean up the line to just get the value
                # logic: remove 'export GEMINI_API_KEY=', remove quotes, trim whitespace
                EXTRACTED_KEY=$(echo "$KEY_IN_FILE" | sed -E 's/^export GEMINI_API_KEY=//' | tr -d '"' | tr -d "'")
                
                if [ -n "$EXTRACTED_KEY" ]; then
                    export GEMINI_API_KEY="$EXTRACTED_KEY"
                    break
                fi
            fi
        fi
    done
fi

# 3. Final check
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Auto-Doc Agent: GEMINI_API_KEY not found in .env or shell profiles. Documentation sync skipped."
    exit 0
fi

# Run the python script using the dedicated venv
if [ -f .auto-doc/venv/bin/python ]; then
    .auto-doc/venv/bin/python .auto-doc/scripts/auto_doc.py
else
    echo "❌ Error: Virtual environment not found at .auto-doc/venv"
    echo "Please run install_hook.sh to set it up."
    exit 1
fi
