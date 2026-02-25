#!/bin/bash

# Gemini ASO Skill Uninstaller
# This script removes the gemini-aso skill from the user scope.

set -e

echo "📦 Uninstalling gemini-aso skill..."

if ! command -v gemini &> /dev/null; then
    echo "❌ Error: Gemini CLI is not installed."
    exit 1
fi

gemini skills uninstall gemini-aso --scope user

echo ""
echo "✅ Uninstallation Successful!"
echo "----------------------------------------------------"
echo "IMPORTANT: You MUST reload your skills to reflect this change."
echo "Run the following command inside your Gemini CLI session:"
echo ""
echo "  /skills reload"
echo "----------------------------------------------------"
