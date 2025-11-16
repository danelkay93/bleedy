#!/usr/bin/env python3
"""
Branch Manager - Automated branch and environment management for Bleedy project

This script manages:
- Branch lifecycle (creation, deletion, stale branch detection)
- Azure Static Web App staging environment cleanup
- PR-based staging environment tracking
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GitHubAPI:
    """Wrapper for GitHub CLI commands"""

    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo
        self.repo_full = f"{owner}/{repo}"

    def run_command(self, cmd: List[str]) -> str:
        """Execute a command and return output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}")
            logger.error(f"Error: {e.stderr}")
            raise

    def get_open_prs(self) -> List[Dict]:
        """Get list of open pull requests"""
        logger.info("Fetching open pull requests...")
        cmd = [
            "gh", "pr", "list",
            "--repo", self.repo_full,
            "--state", "open",
            "--json", "number,title,headRefName,createdAt,author"
        ]
        output = self.run_command(cmd)
        return json.loads(output) if output else []

    def get_closed_prs(self, days: int = 7) -> List[Dict]:
        """Get recently closed pull requests"""
        logger.info(f"Fetching PRs closed in last {days} days...")
        cmd = [
            "gh", "pr", "list",
            "--repo", self.repo_full,
            "--state", "closed",
            "--limit", "100",
            "--json", "number,title,headRefName,closedAt,merged"
        ]
        output = self.run_command(cmd)
        prs = json.loads(output) if output else []

        # Filter by date
        cutoff = datetime.now() - timedelta(days=days)
        recent_prs = []
        for pr in prs:
            if pr.get('closedAt'):
                closed_date = datetime.fromisoformat(pr['closedAt'].replace('Z', '+00:00'))
                if closed_date > cutoff:
                    recent_prs.append(pr)

        return recent_prs

    def get_branches(self) -> List[str]:
        """Get list of remote branches"""
        logger.info("Fetching branches...")
        cmd = ["gh", "api", f"/repos/{self.repo_full}/branches", "--jq", ".[].name"]
        output = self.run_command(cmd)
        return output.split('\n') if output else []

    def delete_branch(self, branch: str, dry_run: bool = False) -> bool:
        """Delete a remote branch"""
        if dry_run:
            logger.info(f"[DRY RUN] Would delete branch: {branch}")
            return True

        try:
            logger.info(f"Deleting branch: {branch}")
            cmd = ["gh", "api", "-X", "DELETE", f"/repos/{self.repo_full}/git/refs/heads/{branch}"]
            self.run_command(cmd)
            return True
        except Exception as e:
            logger.error(f"Failed to delete branch {branch}: {e}")
            return False


class StagingEnvironmentManager:
    """Manages Azure Static Web App staging environments"""

    def __init__(self, github_api: GitHubAPI):
        self.github = github_api

    def identify_orphaned_environments(self, dry_run: bool = False) -> List[int]:
        """
        Identify staging environments that no longer have associated PRs

        Azure Static Web Apps creates staging environments for each PR.
        When a PR is closed, the environment should be cleaned up.
        """
        logger.info("Identifying orphaned staging environments...")

        open_prs = self.github.get_open_prs()
        open_pr_numbers = [pr['number'] for pr in open_prs]

        logger.info(f"Found {len(open_pr_numbers)} open PRs: {open_pr_numbers}")

        # In a real implementation, we would query Azure API to list environments
        # For now, we'll use the PR list to identify what SHOULD exist

        # Get recently closed PRs
        closed_prs = self.github.get_closed_prs(days=1)
        potentially_orphaned = [pr['number'] for pr in closed_prs]

        if potentially_orphaned:
            logger.info(f"PRs recently closed (potential orphaned environments): {potentially_orphaned}")
        else:
            logger.info("No recently closed PRs found")

        return potentially_orphaned

    def cleanup_staging_environments(self, dry_run: bool = False) -> Dict:
        """
        Clean up staging environments for closed PRs

        Note: Azure Static Web Apps automatically cleans up environments when PRs close.
        This method provides visibility and can trigger manual cleanup if needed.
        """
        logger.info("Starting staging environment cleanup...")

        orphaned = self.identify_orphaned_environments(dry_run)
        open_prs = self.github.get_open_prs()

        stats = {
            'active_environments': len(open_prs),
            'recently_closed': len(orphaned),
            'dry_run': dry_run
        }

        logger.info(f"Cleanup summary: {stats}")

        if len(open_prs) > 8:
            logger.warning(f"High number of active staging environments: {len(open_prs)}")
            logger.warning("Consider closing or merging some PRs to free up slots")

        return stats


class BranchManager:
    """Main branch management orchestrator"""

    def __init__(self, owner: str, repo: str):
        self.github = GitHubAPI(owner, repo)
        self.staging_mgr = StagingEnvironmentManager(self.github)

    def find_stale_branches(self, days: int = 30) -> List[str]:
        """
        Find branches that haven't been updated recently

        This is a placeholder - actual implementation would check last commit date
        """
        logger.info(f"Finding branches stale for more than {days} days...")

        # Get all branches
        branches = self.github.get_branches()

        # Filter out protected branches
        protected = ['master', 'main', 'develop']
        candidates = [b for b in branches if b not in protected]

        # In a real implementation, we'd check last commit date via API
        logger.info(f"Found {len(candidates)} non-protected branches")

        return candidates

    def cleanup_merged_branches(self, dry_run: bool = False) -> Dict:
        """Clean up branches for merged PRs"""
        logger.info("Cleaning up merged PR branches...")

        closed_prs = self.github.get_closed_prs(days=7)
        merged_branches = [
            pr['headRefName'] for pr in closed_prs
            if pr.get('merged', False)
        ]

        deleted = []
        failed = []

        for branch in merged_branches:
            if branch in ['master', 'main', 'develop']:
                continue

            if self.github.delete_branch(branch, dry_run):
                deleted.append(branch)
            else:
                failed.append(branch)

        return {
            'deleted': deleted,
            'failed': failed,
            'dry_run': dry_run
        }

    def run_full_cleanup(self, dry_run: bool = False) -> Dict:
        """Run comprehensive cleanup"""
        logger.info("=" * 60)
        logger.info("Starting comprehensive branch and environment cleanup")
        logger.info("=" * 60)

        results = {}

        # Cleanup merged branches
        results['branches'] = self.cleanup_merged_branches(dry_run)

        # Cleanup staging environments
        results['staging'] = self.staging_mgr.cleanup_staging_environments(dry_run)

        logger.info("=" * 60)
        logger.info("Cleanup complete")
        logger.info(f"Branches deleted: {len(results['branches']['deleted'])}")
        logger.info(f"Active staging environments: {results['staging']['active_environments']}")
        logger.info("=" * 60)

        return results


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Branch and environment management')
    parser.add_argument('--owner', default='danelkay93', help='Repository owner')
    parser.add_argument('--repo', default='bleedy', help='Repository name')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode (no changes)')
    parser.add_argument('--action', choices=['cleanup', 'status', 'branches', 'staging'],
                       default='cleanup', help='Action to perform')

    args = parser.parse_args()

    try:
        manager = BranchManager(args.owner, args.repo)

        if args.action == 'cleanup':
            results = manager.run_full_cleanup(dry_run=args.dry_run)
            print(json.dumps(results, indent=2))
        elif args.action == 'status':
            open_prs = manager.github.get_open_prs()
            print(f"Open PRs: {len(open_prs)}")
            for pr in open_prs:
                print(f"  #{pr['number']}: {pr['title']} ({pr['headRefName']})")
        elif args.action == 'branches':
            stale = manager.find_stale_branches()
            print(f"Stale branches: {len(stale)}")
            for branch in stale[:10]:  # Show first 10
                print(f"  {branch}")
        elif args.action == 'staging':
            results = manager.staging_mgr.cleanup_staging_environments(args.dry_run)
            print(json.dumps(results, indent=2))

        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
