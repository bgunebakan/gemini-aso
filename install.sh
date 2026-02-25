#!/bin/bash

# Gemini ASO Skill Installer
# This script installs the gemini-aso skill and verifies dependencies.

set -e

echo "🔍 Checking dependencies..."

# Check for Gemini CLI
if ! command -v gemini &> /dev/null; then
    echo "❌ Error: Gemini CLI is not installed."
    echo "Please install it first: npm install -g @google/gemini-cli"
    exit 1
fi

# Check for Python 3 (required by this skill)
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required for this skill but was not found."
    echo "Please install Python 3: https://www.python.org/downloads/"
    exit 1
fi

echo "🧪 Running automated tests..."
if ! python3 -m unittest discover tests &> /dev/null; then
    echo "❌ Error: Automated tests failed. Aborting installation."
    python3 -m unittest discover tests
    exit 1
fi
echo "✅ Tests passed!"

echo "📦 Installing gemini-aso skill..."

# Check if the .skill file exists
if [ -f "gemini-aso.skill" ]; then
    gemini skills install gemini-aso.skill --scope user
else
    echo "❌ Error: gemini-aso.skill not found in current directory."
    echo "Please run this script from the root of the gemini-aso folder."
    exit 1
fi

echo ""
echo "✅ Installation Successful!"
echo "----------------------------------------------------"
echo "IMPORTANT: You MUST reload your skills to activate them."
echo "Run the following command inside your Gemini CLI session:"
echo ""
echo "  /skills reload"
echo "----------------------------------------------------"
