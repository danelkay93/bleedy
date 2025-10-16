#!/usr/bin/env python3
"""
Post-Merge Cleanup Script

This script automates the cleanup of consolidated PRs and their branches
after a consolidation PR has been merged. It uses Plumbum for command
execution and PyGithub for GitHub API interactions.

Usage:
    python post_merge_cleanup.py --pr-number <PR_NUMBER> [--dry-run]

Environment Variables:
    GITHUB_TOKEN: GitHub personal access token with repo permissions
    GITHUB_REPOSITORY: Repository in format "owner/repo"
"""

import argparse
import os
import sys
from typing import List, Optional

from plumbum import local, FG
from plumbum.cmd import git
from github import Github, GithubException

# Constants
DEFAULT_CONSOLIDATED_PR_NUMBERS = [1, 7, 8, 10, 12, 14, 15]
DEFAULT_CONSOLIDATED_BRANCHES = [
    'refactor-cleanup',
    'phase1-refactor-pyscript-deps',
    'fix/eslint-errors',
    'snyk-upgrade-element-plus-2.9.1',
    'snyk-upgrade-element-plus-2.9.5',
    'snyk-upgrade-element-plus-2.10.5'
]


def get_github_client() -> Github:
    """Initialize and return GitHub client."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    return Github(token)


def get_repository_name() -> str:
    """Get repository name from environment or git config."""
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not repo:
        try:
            # Try to get from git remote
            remote_url = git('config', '--get', 'remote.origin.url').strip()
            # Parse repository from URL (handles both HTTPS and SSH)
            if 'github.com' in remote_url:
                repo = remote_url.split('github.com')[1].strip('/:').replace('.git', '')
        except Exception as e:
            raise ValueError(
                f"Could not determine repository name. Set GITHUB_REPOSITORY env var. Error: {e}"
            )
    return repo


def close_consolidated_prs(
    gh: Github,
    repo_name: str,
    pr_numbers: List[int],
    consolidation_pr_number: int,
    dry_run: bool = False
) -> None:
    """Close the consolidated PRs with appropriate comments."""
    repo = gh.get_repo(repo_name)
    
    for pr_number in pr_numbers:
        try:
            pr = repo.get_pull(pr_number)
            
            if pr.state == 'open':
                comment = (
                    f"This PR has been consolidated into #{consolidation_pr_number} "
                    f"and merged to master.\n\n"
                    f"All changes from this PR are included in the consolidated merge. "
                    f"Closing as completed."
                )
                
                if dry_run:
                    print(f"[DRY RUN] Would close PR #{pr_number} with comment: {comment}")
                else:
                    pr.create_issue_comment(comment)
                    pr.edit(state='closed')
                    print(f"✅ Closed PR #{pr_number}")
            else:
                print(f"ℹ️  PR #{pr_number} is already {pr.state}")
                
        except GithubException as e:
            print(f"⚠️  Could not process PR #{pr_number}: {e.data.get('message', str(e))}")


def delete_branches(
    gh: Github,
    repo_name: str,
    branches: List[str],
    dry_run: bool = False
) -> None:
    """Delete the consolidated branches."""
    repo = gh.get_repo(repo_name)
    
    for branch in branches:
        try:
            if dry_run:
                print(f"[DRY RUN] Would delete branch: {branch}")
            else:
                ref = repo.get_git_ref(f"heads/{branch}")
                ref.delete()
                print(f"✅ Deleted branch: {branch}")
                
        except GithubException as e:
            if e.status == 404:
                print(f"ℹ️  Branch {branch} not found (may already be deleted)")
            else:
                print(f"⚠️  Could not delete branch {branch}: {e.data.get('message', str(e))}")


def add_cleanup_summary(
    gh: Github,
    repo_name: str,
    consolidation_pr_number: int,
    dry_run: bool = False
) -> None:
    """Add a summary comment to the consolidation PR."""
    repo = gh.get_repo(repo_name)
    
    comment = (
        "## 🧹 Post-Merge Cleanup Complete\n\n"
        "✅ Consolidated PRs have been closed\n"
        "✅ Obsolete branches have been deleted\n\n"
        "The repository is now clean and ready for future development."
    )
    
    try:
        if dry_run:
            print(f"[DRY RUN] Would add summary comment to PR #{consolidation_pr_number}")
        else:
            issue = repo.get_issue(consolidation_pr_number)
            issue.create_comment(comment)
            print(f"✅ Added cleanup summary to PR #{consolidation_pr_number}")
    except GithubException as e:
        print(f"⚠️  Could not add summary comment: {e.data.get('message', str(e))}")


def main():
    """Main entry point for the post-merge cleanup script."""
    parser = argparse.ArgumentParser(
        description="Cleanup consolidated PRs and branches after merge"
    )
    parser.add_argument(
        '--pr-number',
        type=int,
        required=True,
        help='The consolidation PR number that was merged'
    )
    parser.add_argument(
        '--pr-numbers-to-close',
        type=int,
        nargs='+',
        default=DEFAULT_CONSOLIDATED_PR_NUMBERS,
        help='PR numbers to close (space-separated)'
    )
    parser.add_argument(
        '--branches-to-delete',
        nargs='+',
        default=DEFAULT_CONSOLIDATED_BRANCHES,
        help='Branch names to delete (space-separated)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without making actual changes'
    )
    
    args = parser.parse_args()
    
    try:
        print("🚀 Starting post-merge cleanup...")
        if args.dry_run:
            print("⚠️  DRY RUN MODE - No actual changes will be made")
        
        # Initialize GitHub client
        gh = get_github_client()
        repo_name = get_repository_name()
        print(f"📦 Repository: {repo_name}")
        print(f"🔗 Consolidation PR: #{args.pr_number}")
        
        # Close consolidated PRs
        print("\n📝 Closing consolidated PRs...")
        close_consolidated_prs(
            gh,
            repo_name,
            args.pr_numbers_to_close,
            args.pr_number,
            args.dry_run
        )
        
        # Delete branches
        print("\n🗑️  Deleting consolidated branches...")
        delete_branches(
            gh,
            repo_name,
            args.branches_to_delete,
            args.dry_run
        )
        
        # Add summary comment
        print("\n📋 Adding cleanup summary...")
        add_cleanup_summary(
            gh,
            repo_name,
            args.pr_number,
            args.dry_run
        )
        
        print("\n✨ Post-merge cleanup completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
