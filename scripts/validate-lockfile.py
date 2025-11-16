#!/usr/bin/env python3
"""
Lock File Validation Script
Validates that package-lock.json is in sync with package.json
"""

import sys
import json
import subprocess
from pathlib import Path


def error(message: str) -> None:
    """Print error message in GitHub Actions format"""
    print(f"::error::{message}")


def main() -> int:
    """Main validation function"""
    print("=== Lock File Validation ===")
    
    # Check if package-lock.json exists
    lockfile = Path("package-lock.json")
    if not lockfile.exists():
        error("package-lock.json not found!")
        print("Please run 'npm install' to generate the lock file.")
        return 1
    
    print("✅ package-lock.json exists")
    
    # Check if package.json exists
    packagefile = Path("package.json")
    if not packagefile.exists():
        error("package.json not found!")
        return 1
    
    print("✅ package.json exists")
    
    # Validate lock file format
    try:
        with lockfile.open() as f:
            lockdata = json.load(f)
    except json.JSONDecodeError:
        error("package-lock.json is not valid JSON")
        return 1
    
    print("✅ package-lock.json is valid JSON")
    
    # Check if lock file version is supported
    lock_version = lockdata.get("lockfileVersion", 0)
    if lock_version < 2:
        print(f"::warning::Old lock file version detected (v{lock_version}). "
              "Consider regenerating with newer npm.")
    
    print(f"✅ Lock file version: {lock_version}")
    
    # Perform dry-run to check if lock file is in sync
    print("Checking if lock file is in sync with package.json...")
    
    try:
        result = subprocess.run(
            ["npm", "ci", "--dry-run"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("✅ Lock file is in sync with package.json")
            return 0
        else:
            error("Lock file is out of sync with package.json")
            print("")
            print("To fix this issue, run:")
            print("  rm package-lock.json")
            print("  npm install")
            print("  git add package-lock.json")
            print("  git commit -m 'chore: regenerate package-lock.json'")
            return 1
            
    except FileNotFoundError:
        error("npm command not found")
        return 1
    except Exception as e:
        error(f"Error running npm ci: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
