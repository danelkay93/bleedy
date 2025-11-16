#!/usr/bin/env python3
"""
Post-create command for devcontainer
Runs after container is created to set up the development environment
"""

import sys
from pathlib import Path
from plumbum import local, colors
from plumbum.cmd import npm, git, gh, python3, bash
import subprocess


def print_status(message: str) -> None:
    """Print blue status message"""
    print(colors.blue | f"[SETUP] {message}")


def print_success(message: str) -> None:
    """Print green success message"""
    print(colors.green | f"[✓] {message}")


def print_warning(message: str) -> None:
    """Print yellow warning message"""
    print(colors.yellow | f"[!] {message}")


def make_executable(pattern: str, base_dir: Path) -> None:
    """
    Make files matching pattern executable.
    Only processes files that actually exist to avoid errors.
    
    Args:
        pattern: Glob pattern (e.g., "*.sh", "*.py")
        base_dir: Base directory to search in
    """
    if not base_dir.exists():
        return
    
    files = list(base_dir.glob(pattern))
    for file in files:
        if file.is_file():
            file.chmod(0o755)
            print_success(f"Made {file.relative_to(Path.cwd())} executable")


def command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH"""
    try:
        subprocess.run(
            ["command", "-v", cmd],
            shell=True,
            executable="/bin/bash",
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def main() -> int:
    """Main setup function"""
    print("🚀 Setting up Bleedy development environment for multi-agent collaboration...")
    print()
    
    # Get workspace root
    workspace = Path.cwd()
    
    # Install npm dependencies
    print_status("Installing npm dependencies...")
    try:
        npm["install"]()
        print_success("npm dependencies installed")
    except Exception as e:
        print_warning(f"Failed to install npm dependencies: {e}")
        return 1
    
    # Configure git for PR access
    print_status("Configuring git for PR refs...")
    try:
        # Use || true equivalent by catching exceptions
        try:
            git["config", "--add", "remote.origin.fetch", "+refs/pull/*/head:refs/remotes/origin/pr/*"]()
        except:
            pass
        try:
            git["config", "--add", "remote.origin.fetch", "+refs/pull/*/merge:refs/remotes/origin/pr-merge/*"]()
        except:
            pass
        print_success("Git configured for PR access")
    except Exception as e:
        print_warning(f"Failed to configure git: {e}")
    
    # Try to fetch PR refs (may fail if not authenticated, which is OK)
    print_status("Attempting to fetch PR refs...")
    try:
        git["fetch", "origin"](retcode=None, stderr=subprocess.DEVNULL)
        print_success("PR refs fetched")
    except:
        print_warning("Could not fetch PR refs (authentication may be needed)")
    
    # Set up git user if not configured
    try:
        user_name = git["config", "user.name"]().strip()
        if not user_name:
            raise ValueError("Empty user.name")
    except:
        print_warning("Git user.name not set. Set it with: git config user.name 'Your Name'")
    
    try:
        user_email = git["config", "user.email"]().strip()
        if not user_email:
            raise ValueError("Empty user.email")
    except:
        print_warning("Git user.email not set. Set it with: git config user.email 'your.email@example.com'")
    
    # Verify GitHub CLI
    if command_exists("gh"):
        print_success("GitHub CLI (gh) is available")
        # Check auth status (won't fail if not authenticated)
        try:
            gh["auth", "status"](stderr=subprocess.DEVNULL)
            print_success("GitHub CLI is authenticated")
        except:
            print_warning("GitHub CLI not authenticated. Run: gh auth login")
    else:
        print_warning("GitHub CLI (gh) is not available")
    
    # Verify Python
    if command_exists("python3"):
        try:
            python_version = python3["--version"]().strip()
            print_success(f"Python is available: {python_version}")
        except:
            print_success("Python is available")
    else:
        print_warning("Python is not available")
    
    # Make scripts executable
    print_status("Making scripts executable...")
    scripts_dir = workspace / "scripts"
    automation_dir = workspace / "automation"
    
    # Use Pathlib to safely handle file existence
    make_executable("*.sh", scripts_dir)
    make_executable("*.py", scripts_dir)
    make_executable("*.py", automation_dir)
    
    print_success("Scripts are executable")
    
    # Run agent environment setup
    agent_setup_script = workspace / "scripts" / "setup-agent-environment.sh"
    if agent_setup_script.exists():
        print_status("Running agent environment setup...")
        try:
            bash[str(agent_setup_script)]()
        except Exception as e:
            print_warning(f"Agent environment setup failed: {e}")
    else:
        print_warning("Agent environment setup script not found")
    
    # Verify build
    print_status("Verifying build...")
    try:
        npm["run", "build"](stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("Build verification passed")
    except:
        print_warning("Build verification failed - you may need to run 'npm run build' manually")
    
    # Print summary
    print()
    print(colors.green | "========================================")
    print(colors.green | "✓ Development environment ready!")
    print(colors.green | "========================================")
    print()
    print("Quick start commands:")
    print("  npm run dev          - Start development server")
    print("  npm run build        - Build for production")
    print("  npm run lint         - Run ESLint")
    print("  npm run format       - Format code with Prettier")
    print()
    print("Multi-agent collaboration:")
    print("  See: .github/AGENT_COLLABORATION.md")
    print("  See: .github/ACCESSING_PR_REVIEWS.md")
    print()
    print("For GitHub operations:")
    print("  gh auth login        - Authenticate with GitHub")
    print("  gh pr list           - List pull requests")
    print("  gh pr view <number>  - View PR details")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
