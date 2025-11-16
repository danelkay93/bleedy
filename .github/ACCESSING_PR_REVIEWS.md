# Accessing PR Reviews Programmatically - Guide for AI Agents

## Overview

This document provides guidance for AI agents attempting to access GitHub Pull Request reviews programmatically within the repository environment.

## Current Environment Limitations

### What's NOT Available

1. **GitHub CLI (`gh`)** - Not installed in the environment
   - Commands like `gh pr view`, `gh api` will fail with `FileNotFoundError`
   - The `automation/branch_manager.py` script assumes `gh` is available but may fail in some environments

2. **Direct HTTP API Access** - Path format unclear
   - Attempted paths that failed:
     - `http://127.0.0.1:19866/api/repos/{owner}/{repo}/pulls`
     - `http://127.0.0.1:19866/repos/{owner}/{repo}/pulls`
   - All returned: `400 Bad Request - Invalid path format`

3. **Git Protocol for PRs** - Not configured
   - No `refs/pull/*` references found
   - No PR fetch configuration in git config

### What IS Available

1. **Git commands** - Full git access to repository
2. **curl** - HTTP client available
3. **Python 3** - Available for scripting
4. **File system access** - Full repository access
5. **Git history** - Can search commits for review-related messages

## Recommended Approaches

### Option 1: Request from User (MOST RELIABLE)

Since direct API access has limitations, the most reliable approach is to request review information directly from the user:

```markdown
I cannot access PR reviews programmatically due to environment limitations.
Could you please provide:
1. The review status (Approved / Changes Requested / Pending)
2. Any review comments from @copilot, @coderabbitai, or @codex
3. Whether I should proceed with the merge
```

### Option 2: Check Git Commit Messages

Search git history for review-related information:

```bash
# Search for review mentions
git log --all --grep="review\|@copilot\|@coderabbitai\|approved\|changes requested" -i --oneline

# Check for review-related commits
git show <commit>:REVIEW_REQUEST.md
git show <commit>:REVIEW_RESPONSE.md
```

### Option 3: Check for Review Files in Repository

Some workflows may leave review artifacts:

```bash
# Look for review-related files
find . -name "*review*" -o -name "*feedback*" -type f

# Check .github directory for review templates or responses
ls -la .github/*review* .github/*response*
```

### Option 4: Use MCP Tools (If Available)

Some agents (like GitHub Copilot) may have Model Context Protocol (MCP) tools for GitHub operations:

- Check if MCP GitHub tools are available
- Use `report_progress` or similar tools to query PR status
- This varies by agent implementation

## For Future Environment Setup

To enable programmatic PR review access, one of the following should be configured:

### Option A: Install GitHub CLI

```bash
# Install gh CLI in the container
apt-get update && apt-get install -y gh

# Or download binary
wget https://github.com/cli/cli/releases/download/v2.40.0/gh_2.40.0_linux_amd64.deb
dpkg -i gh_2.40.0_linux_amd64.deb

# Authenticate (if needed)
gh auth login
```

### Option B: Configure Git to Fetch PRs

Add PR fetch configuration to git:

```bash
git config --add remote.origin.fetch '+refs/pull/*/head:refs/pull/origin/*'
git fetch origin
```

Then access PR refs:

```bash
git log refs/pull/origin/36/head
git diff master...refs/pull/origin/36/head
```

### Option C: Clarify Internal API Path Format

Document the correct internal API path format for the environment:

```bash
# What is the correct path?
# Examples that should work:
curl "http://127.0.0.1:PORT/??/repos/{owner}/{repo}/pulls/{number}/reviews"

# Once identified, document here
```

## Implementation: PR Review Access Script

A Python script has been created at `scripts/get_pr_reviews.py` that demonstrates the intended approach using `gh` CLI:

```python
# Usage (if gh CLI is available):
python3 scripts/get_pr_reviews.py 36
python3 scripts/get_pr_reviews.py claude/update-documentation-integration-011CULn7AGnkyHBdk8qWi4qx
```

**Current Status**: Script fails because `gh` is not installed

## Agent-Specific Approaches

### Claude Code

- **Limitation**: Cannot access external URLs or internal API (path format unclear)
- **Limitation**: `gh` CLI not available in environment
- **Capability**: Can use git commands, search history, read files
- **Recommendation**: Request review information from user
- **Fallback**: Search git history for review mentions

### GitHub Copilot

- **Capability**: May have MCP tools for GitHub operations
- **Capability**: Can use `report_progress` which might include PR status
- **Recommendation**: Use MCP tools if available, otherwise request from user

### CodeRabbit

- **Capability**: Automated review system, likely has its own API access
- **Capability**: May be able to query its own review status
- **Recommendation**: Use internal CodeRabbit APIs

## Examples

### Checking for Review Request Documents

```bash
# Check current branch for review requests
git show HEAD:REVIEW_REQUEST.md 2>/dev/null

# Check PR base branch
git show origin/copilot/consolidate-devops-ci-cd:REVIEW_REQUEST.md 2>/dev/null
```

### Searching Git History for Reviews

```bash
# Find commits mentioning reviews
git log --all --oneline | grep -i "review\|approved\|changes"

# Show specific review-related commit
git show <commit-hash>
```

### Checking Branch Metadata

```bash
# Get branch information
git branch -vv | grep "claude/update"

# Check branch tracking
git log --oneline origin/claude/update-documentation-integration-011CULn7AGnkyHBdk8qWi4qx -5
```

## Workaround: Manual Review Workflow

Until programmatic access is established, use this manual workflow:

1. **Agent creates PR** and documents changes
2. **Agent requests reviews** via @mentions in PR description
3. **User or other agents provide feedback** in PR comments
4. **User pastes feedback** into a message to the agent
5. **Agent addresses feedback** and documents resolution
6. **User confirms** when ready to merge
7. **Agent performs merge** and cleanup

## Documentation Updates Needed

When PR review access is established, update:

1. **This document** - Add working examples
2. **AGENT_COLLABORATION.md** - Update network access section
3. **Scripts** - Update `scripts/get_pr_reviews.py` to work
4. **Automation** - Update `automation/branch_manager.py` if needed

## Conclusion

Current environment **does not support** programmatic PR review access due to:
- Missing `gh` CLI
- Unclear internal API path format
- No git PR refs configured

**Recommended Action**: Request review information from users until environment is configured.

---

**Last Updated**: 2025-10-21
**Created by**: Claude Code
**Status**: Environment limitation documented, workarounds provided
