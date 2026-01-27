#!/bin/bash
# Auto-Doc Hook Installer
# Copies the hook scripts to the local .git/hooks directory

echo "🔧 Installing Auto-Doc Git Hooks..."

# 1. Setup Python Environment
if [ ! -d ".auto-doc/venv" ]; then
    echo "📦 Creating virtual environment in .auto-doc/venv..."
    python3 -m venv .auto-doc/venv
fi

echo "⬇️  Installing 'autodoc' package..."
.auto-doc/venv/bin/pip install -e . > /dev/null

# 2. Setup Hook Scripts
HOOK_PATH=".git/hooks/post-commit"

cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash
# Post-commit hook to trigger Auto-Doc Agent

# 1. Load Environment Variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 2. Fallback: Check shell profiles if key is missing
if [ -z "$GEMINI_API_KEY" ]; then
    CONFIG_FILES=("$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile")
    for file in "${CONFIG_FILES[@]}"; do
        if [ -f "$file" ]; then
            KEY_IN_FILE=$(grep "export GEMINI_API_KEY" "$file" | head -n 1)
            if [ -n "$KEY_IN_FILE" ]; then
                EXTRACTED_KEY=$(echo "$KEY_IN_FILE" | sed -E 's/^export GEMINI_API_KEY=//' | tr -d \'\"\' | tr -d \"\'\")
                if [ -n "$EXTRACTED_KEY" ]; then
                    export GEMINI_API_KEY="$EXTRACTED_KEY"
                    break
                fi
            fi
        fi
    done
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Auto-Doc Agent: GEMINI_API_KEY not found. Skipping."
    exit 0
fi

echo "🤖 Git Hook: Triggering Auto-Documentation..."
# Run the CLI tool from the venv
./.auto-doc/venv/bin/autodoc
EOF

chmod +x "$HOOK_PATH"

echo "✅ Hook installed via $HOOK_PATH"
echo "🎉 You can now commit changes to src/ and watch docs/API.md update automatically!"
