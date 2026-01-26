#!/bin/bash

# Auto-Doc Hook Installer
# Copies the hook scripts to the local .git/hooks directory

echo "🔧 Installing Auto-Doc Git Hooks..."

# Ensure the scripts are executable
chmod +x .agent/scripts/auto_doc.py
chmod +x .agent/scripts/auto_doc_wrapper.sh

# Create the post-commit hook
HOOK_PATH=".git/hooks/post-commit"

cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash
# Post-commit hook to trigger Auto-Doc Agent

echo "🤖 Git Hook: Triggering Auto-Documentation..."
# Run the wrapper from the project root
./.agent/scripts/auto_doc_wrapper.sh
EOF

chmod +x "$HOOK_PATH"

echo "✅ Hook installed via $HOOK_PATH"
echo "🎉 You can now commit changes to src/ and watch docs/API.md update automatically!"
