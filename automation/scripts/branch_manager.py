#!/usr/bin/env python3
"""
Branch Management Script

This script automates branch management tasks including:
- Listing branches by age, activity, and status
- Cleaning up stale branches
- Creating branch protection rules
- Syncing branches with upstream

Usage:
    python branch_manager.py <command> [options]

Commands:
    list        - List branches with filtering options
    cleanup     - Delete stale branches
    protect     - Set up branch protection rules
    sync        - Sync branch with upstream

Environment Variables:
    GITHUB_TOKEN: GitHub personal access token with repo permissions
    GITHUB_REPOSITORY: Repository in format "owner/repo"
"""

import argparse
import sys
from datetime import datetime, timedelta
from typing import List, Optional

from plumbum import local, FG
from plumbum.cmd import git
from github import Github, GithubException


def get_github_client() -> Github:
    """Initialize and return GitHub client."""
    import os
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    return Github(token)


def get_repository_name() -> str:
    """Get repository name from environment or git config."""
    import os
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not repo:
        try:
            # Try to get from git remote
            remote_url = git('config', '--get', 'remote.origin.url').strip()
            if 'github.com' in remote_url:
                repo = remote_url.split('github.com')[1].strip('/:').replace('.git', '')
        except Exception as e:
            raise ValueError(
                f"Could not determine repository name. Set GITHUB_REPOSITORY env var. Error: {e}"
            )
    return repo


def list_branches(
    gh: Github,
    repo_name: str,
    older_than_days: Optional[int] = None,
    pattern: Optional[str] = None
) -> None:
    """List branches with optional filtering."""
    repo = gh.get_repo(repo_name)
    branches = repo.get_branches()
    
    print("📋 Branch List\n")
    print(f"{'Branch Name':<40} {'Last Commit':<20} {'Protected':<10}")
    print("-" * 70)
    
    cutoff_date = None
    if older_than_days:
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
    
    for branch in branches:
        # Filter by pattern if provided
        if pattern and pattern not in branch.name:
            continue
        
        commit = repo.get_commit(branch.commit.sha)
        commit_date = commit.commit.author.date
        
        # Filter by age if provided
        if cutoff_date and commit_date > cutoff_date:
            continue
        
        # Format date
        days_old = (datetime.now() - commit_date.replace(tzinfo=None)).days
        date_str = f"{days_old} days ago"
        
        protected_str = "Yes" if branch.protected else "No"
        
        print(f"{branch.name:<40} {date_str:<20} {protected_str:<10}")


def cleanup_branches(
    gh: Github,
    repo_name: str,
    older_than_days: int,
    pattern: Optional[str] = None,
    exclude: Optional[List[str]] = None,
    dry_run: bool = False
) -> None:
    """Delete stale branches."""
    repo = gh.get_repo(repo_name)
    branches = repo.get_branches()
    
    cutoff_date = datetime.now() - timedelta(days=older_than_days)
    exclude = exclude or ['master', 'main', 'develop', 'staging', 'production']
    
    print(f"🗑️  Cleaning up branches older than {older_than_days} days\n")
    if dry_run:
        print("⚠️  DRY RUN MODE - No actual changes will be made\n")
    
    deleted_count = 0
    skipped_count = 0
    
    for branch in branches:
        # Skip excluded branches
        if branch.name in exclude:
            skipped_count += 1
            continue
        
        # Skip protected branches
        if branch.protected:
            print(f"ℹ️  Skipping protected branch: {branch.name}")
            skipped_count += 1
            continue
        
        # Filter by pattern if provided
        if pattern and pattern not in branch.name:
            continue
        
        # Check age
        commit = repo.get_commit(branch.commit.sha)
        commit_date = commit.commit.author.date
        
        if commit_date.replace(tzinfo=None) < cutoff_date:
            if dry_run:
                print(f"[DRY RUN] Would delete branch: {branch.name}")
            else:
                try:
                    ref = repo.get_git_ref(f"heads/{branch.name}")
                    ref.delete()
                    print(f"✅ Deleted branch: {branch.name}")
                    deleted_count += 1
                except GithubException as e:
                    print(f"⚠️  Could not delete {branch.name}: {e.data.get('message', str(e))}")
    
    print(f"\n📊 Summary: {deleted_count} deleted, {skipped_count} skipped")


def protect_branch(
    gh: Github,
    repo_name: str,
    branch_name: str,
    require_reviews: int = 1,
    require_ci: bool = True,
    dry_run: bool = False
) -> None:
    """Set up branch protection rules."""
    repo = gh.get_repo(repo_name)
    
    print(f"🔒 Setting up protection for branch: {branch_name}\n")
    if dry_run:
        print("⚠️  DRY RUN MODE - No actual changes will be made")
    
    try:
        branch = repo.get_branch(branch_name)
        
        protection_kwargs = {
            "strict": True,
            "contexts": ["CI Checks and Build"] if require_ci else []
        }
        
        if require_reviews > 0:
            protection_kwargs["required_approving_review_count"] = require_reviews
        
        if dry_run:
            print(f"[DRY RUN] Would apply protection with settings:")
            print(f"  - Required reviews: {require_reviews}")
            print(f"  - Required CI: {require_ci}")
        else:
            branch.edit_protection(**protection_kwargs)
            print(f"✅ Branch protection applied successfully")
            
    except GithubException as e:
        print(f"❌ Error: {e.data.get('message', str(e))}")


def sync_branch(
    branch_name: str,
    upstream_branch: str = "master",
    dry_run: bool = False
) -> None:
    """Sync branch with upstream."""
    print(f"🔄 Syncing branch '{branch_name}' with '{upstream_branch}'\n")
    if dry_run:
        print("⚠️  DRY RUN MODE - No actual changes will be made")
    
    try:
        # Fetch latest changes
        if dry_run:
            print(f"[DRY RUN] Would fetch from origin")
        else:
            git['fetch', 'origin'] & FG
        
        # Checkout target branch
        if dry_run:
            print(f"[DRY RUN] Would checkout branch: {branch_name}")
        else:
            git['checkout', branch_name] & FG
        
        # Merge upstream
        if dry_run:
            print(f"[DRY RUN] Would merge origin/{upstream_branch} into {branch_name}")
        else:
            git['merge', f'origin/{upstream_branch}'] & FG
            print(f"✅ Successfully synced {branch_name} with {upstream_branch}")
            
    except Exception as e:
        print(f"❌ Error during sync: {e}")


def main():
    """Main entry point for the branch manager script."""
    parser = argparse.ArgumentParser(
        description="Manage GitHub branches with various operations"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List branches')
    list_parser.add_argument(
        '--older-than',
        type=int,
        help='Only show branches older than N days'
    )
    list_parser.add_argument(
        '--pattern',
        help='Filter branches by name pattern'
    )
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Delete stale branches')
    cleanup_parser.add_argument(
        '--older-than',
        type=int,
        required=True,
        help='Delete branches older than N days'
    )
    cleanup_parser.add_argument(
        '--pattern',
        help='Only delete branches matching pattern'
    )
    cleanup_parser.add_argument(
        '--exclude',
        nargs='+',
        help='Branch names to exclude from deletion'
    )
    cleanup_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run'
    )
    
    # Protect command
    protect_parser = subparsers.add_parser('protect', help='Set branch protection')
    protect_parser.add_argument(
        '--branch',
        required=True,
        help='Branch name to protect'
    )
    protect_parser.add_argument(
        '--require-reviews',
        type=int,
        default=1,
        help='Number of required reviews'
    )
    protect_parser.add_argument(
        '--require-ci',
        action='store_true',
        default=False,
        help='Require CI checks to pass'
    )
    protect_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run'
    )
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync branch with upstream')
    sync_parser.add_argument(
        '--branch',
        required=True,
        help='Branch name to sync'
    )
    sync_parser.add_argument(
        '--upstream',
        default='master',
        help='Upstream branch to sync with'
    )
    sync_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Initialize GitHub client for commands that need it
        if args.command in ['list', 'cleanup', 'protect']:
            gh = get_github_client()
            repo_name = get_repository_name()
            print(f"📦 Repository: {repo_name}\n")
        
        # Execute command
        if args.command == 'list':
            list_branches(gh, repo_name, args.older_than, args.pattern)
        
        elif args.command == 'cleanup':
            cleanup_branches(
                gh,
                repo_name,
                args.older_than,
                args.pattern,
                args.exclude,
                args.dry_run
            )
        
        elif args.command == 'protect':
            protect_branch(
                gh,
                repo_name,
                args.branch,
                args.require_reviews,
                args.require_ci,
                args.dry_run
            )
        
        elif args.command == 'sync':
            sync_branch(args.branch, args.upstream, args.dry_run)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
