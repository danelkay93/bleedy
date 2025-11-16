#!/bin/bash
#
# Lock File Validation Script
# Validates that package-lock.json is in sync with package.json
#

set -e

echo "=== Lock File Validation ==="

# Check if package-lock.json exists
if [ ! -f "package-lock.json" ]; then
  echo "::error::package-lock.json not found!"
  echo "Please run 'npm install' to generate the lock file."
  exit 1
fi

echo "✅ package-lock.json exists"

# Check if package.json exists
if [ ! -f "package.json" ]; then
  echo "::error::package.json not found!"
  exit 1
fi

echo "✅ package.json exists"

# Validate lock file format
if ! jq empty package-lock.json 2>/dev/null; then
  echo "::error::package-lock.json is not valid JSON"
  exit 1
fi

echo "✅ package-lock.json is valid JSON"

# Check if lock file version is supported
LOCK_VERSION=$(jq -r '.lockfileVersion // 0' package-lock.json)
if [ "$LOCK_VERSION" -lt 2 ]; then
  echo "::warning::Old lock file version detected (v$LOCK_VERSION). Consider regenerating with newer npm."
fi

echo "✅ Lock file version: $LOCK_VERSION"

# Perform dry-run to check if lock file is in sync
echo "Checking if lock file is in sync with package.json..."

if npm ci --dry-run > /dev/null 2>&1; then
  echo "✅ Lock file is in sync with package.json"
  exit 0
else
  echo "::error::Lock file is out of sync with package.json"
  echo ""
  echo "To fix this issue, run:"
  echo "  rm package-lock.json"
  echo "  npm install"
  echo "  git add package-lock.json"
  echo "  git commit -m 'chore: regenerate package-lock.json'"
  exit 1
fi
