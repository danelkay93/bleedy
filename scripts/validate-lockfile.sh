#!/bin/bash

# Script to validate that package-lock.json is in sync with package.json
# This helps prevent npm ci failures due to lock file being out of sync

set -e

echo "🔍 Validating package-lock.json sync with package.json..."

# Check if package-lock.json exists
if [ ! -f "package-lock.json" ]; then
  echo "❌ Error: package-lock.json not found!"
  echo "Run 'npm install' to generate it."
  exit 1
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
  echo "❌ Error: package.json not found!"
  exit 1
fi

# Create a temporary directory for testing
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Copy package files to temp directory
cp package.json package-lock.json "$TEMP_DIR/"
cd "$TEMP_DIR"

echo "📦 Testing npm ci in isolated environment..."

# Try npm ci - if it fails, the lock file is out of sync
if npm ci --dry-run > /dev/null 2>&1; then
  echo "✅ Lock file is in sync with package.json"
  exit 0
else
  echo "❌ Lock file is NOT in sync with package.json!"
  echo ""
  echo "This usually happens when:"
  echo "  1. package.json was manually edited without running 'npm install'"
  echo "  2. Different npm versions were used to update dependencies"
  echo "  3. Lock file was manually edited (should never be done)"
  echo ""
  echo "To fix this issue:"
  echo "  1. Run: rm package-lock.json"
  echo "  2. Run: npm install"
  echo "  3. Commit the updated package-lock.json"
  echo ""
  echo "⚠️  IMPORTANT: Never manually edit package-lock.json!"
  exit 1
fi
