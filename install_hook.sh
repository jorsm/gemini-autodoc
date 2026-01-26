#!/bin/bash
# Auto-Doc Hook Installer
# Copies the hook scripts to the local .git/hooks directory

echo "🔧 Installing Auto-Doc Git Hooks..."

# 1. Setup Python Environment
if [ ! -d ".auto-doc/venv" ]; then
    echo "📦 Creating virtual environment in .auto-doc/venv..."
    python3 -m venv .auto-doc/venv
fi

echo "⬇️  Installing dependencies..."
.auto-doc/venv/bin/pip install -r .auto-doc/requirements.txt > /dev/null

# 2. Setup Hook Scripts
# Ensure the scripts are executable
chmod +x .auto-doc/scripts/auto_doc.py
chmod +x .auto-doc/scripts/auto_doc_wrapper.sh

# Create the post-commit hook
HOOK_PATH=".git/hooks/post-commit"

cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash
# Post-commit hook to trigger Auto-Doc Agent

echo "🤖 Git Hook: Triggering Auto-Documentation..."
# Run the wrapper from the project root
./.auto-doc/scripts/auto_doc_wrapper.sh
EOF

chmod +x "$HOOK_PATH"

echo "✅ Hook installed via $HOOK_PATH"
echo "🎉 You can now commit changes to src/ and watch docs/API.md update automatically!"
