#!/usr/bin/env python3
"""
Get PR reviews programmatically using GitHub CLI

This script demonstrates how to access PR review information using gh CLI,
which is the recommended approach for agents working within the repository.

Exit Codes:
    0 - PR is approved (success)
    1 - PR is pending review or other state (no decision yet)
    2 - PR has changes requested (action required)

The exit codes are designed for automation that needs to distinguish between
different PR states. For simple success/failure checks, treat any non-zero
exit code as failure. For more sophisticated workflows, use the specific codes:
- 0: Safe to merge (approved)
- 2: Must address feedback (changes requested)  
- 1: Waiting or unknown state (pending/other)

This follows conventions used by tools like `diff` and `grep` where different
non-zero exit codes indicate different types of "failure" or states.
"""

import subprocess
import json
import sys
from typing import Dict, List, Optional


def run_gh_command(args: List[str]) -> str:
    """Execute a gh CLI command and return output"""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        raise


def get_pr_by_branch(branch_name: str) -> Optional[int]:
    """Find PR number by branch name"""
    try:
        output = run_gh_command([
            "pr", "list",
            "--head", branch_name,
            "--json", "number",
            "--jq", ".[0].number"
        ])
        return int(output) if output and output != "null" else None
    except (ValueError, subprocess.CalledProcessError):
        return None


def get_pr_details(pr_number: int) -> Dict:
    """Get detailed PR information including reviews"""
    try:
        output = run_gh_command([
            "pr", "view", str(pr_number),
            "--json", "number,title,state,author,reviews,comments,reviewDecision,baseRefName,headRefName"
        ])
        return json.loads(output)
    except subprocess.CalledProcessError:
        return {}


def get_pr_reviews(pr_number: int) -> List[Dict]:
    """Get reviews for a specific PR"""
    try:
        # Using gh api directly for reviews
        output = run_gh_command([
            "api",
            f"/repos/{{owner}}/{{repo}}/pulls/{pr_number}/reviews",
            "--jq", "."
        ])
        return json.loads(output) if output else []
    except subprocess.CalledProcessError:
        return []


def get_pr_review_comments(pr_number: int) -> List[Dict]:
    """Get review comments (line-specific comments) for a PR"""
    try:
        output = run_gh_command([
            "api",
            f"/repos/{{owner}}/{{repo}}/pulls/{pr_number}/comments",
            "--jq", "."
        ])
        return json.loads(output) if output else []
    except subprocess.CalledProcessError:
        return []


def format_review_summary(pr_details: Dict) -> str:
    """Format PR review information for display"""
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"PR #{pr_details.get('number')}: {pr_details.get('title')}")
    lines.append(f"{'='*80}")
    lines.append(f"State: {pr_details.get('state')}")
    lines.append(f"Author: {pr_details.get('author', {}).get('login', 'Unknown')}")
    lines.append(f"Base: {pr_details.get('baseRefName')} <- Head: {pr_details.get('headRefName')}")
    lines.append(f"Review Decision: {pr_details.get('reviewDecision', 'PENDING')}")
    lines.append("")

    reviews = pr_details.get('reviews', [])
    if reviews:
        lines.append(f"Reviews ({len(reviews)}):")
        lines.append("-" * 80)
        for review in reviews:
            author = review.get('author', {}).get('login', 'Unknown')
            state = review.get('state', 'UNKNOWN')
            submitted_at = review.get('submittedAt', 'Unknown')
            body = review.get('body', '').strip()

            lines.append(f"\n{author} - {state} (submitted: {submitted_at})")
            if body:
                lines.append(f"  Comment: {body}")
    else:
        lines.append("No reviews yet")

    comments = pr_details.get('comments', [])
    if comments:
        lines.append(f"\n\nComments ({len(comments)}):")
        lines.append("-" * 80)
        for comment in comments:
            author = comment.get('author', {}).get('login', 'Unknown')
            body = comment.get('body', '').strip()
            lines.append(f"\n{author}:")
            lines.append(f"  {body[:200]}..." if len(body) > 200 else f"  {body}")

    return "\n".join(lines)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 get_pr_reviews.py <pr_number|branch_name>")
        print("\nExamples:")
        print("  python3 get_pr_reviews.py 36")
        print("  python3 get_pr_reviews.py claude/update-documentation-integration-011CULn7AGnkyHBdk8qWi4qx")
        sys.exit(1)

    arg = sys.argv[1]

    # Try to parse as PR number first
    try:
        pr_number = int(arg)
    except ValueError:
        # Assume it's a branch name
        print(f"Looking up PR for branch: {arg}")
        pr_number = get_pr_by_branch(arg)
        if not pr_number:
            print(f"No PR found for branch: {arg}", file=sys.stderr)
            sys.exit(1)
        print(f"Found PR #{pr_number}")

    # Get PR details
    pr_details = get_pr_details(pr_number)
    if not pr_details:
        print(f"Could not fetch details for PR #{pr_number}", file=sys.stderr)
        sys.exit(1)

    # Display summary
    print(format_review_summary(pr_details))

    # Return exit code based on review decision
    # Exit codes allow automation to distinguish between different PR states:
    #   0 = APPROVED (safe to merge)
    #   2 = CHANGES_REQUESTED (must address feedback)
    #   1 = PENDING or other (waiting or unknown state)
    decision = pr_details.get('reviewDecision', '')
    if decision == 'APPROVED':
        sys.exit(0)  # Success - PR approved
    elif decision == 'CHANGES_REQUESTED':
        sys.exit(2)  # Action required - changes requested
    else:
        sys.exit(1)  # Waiting - pending review or unknown state


if __name__ == "__main__":
    main()
