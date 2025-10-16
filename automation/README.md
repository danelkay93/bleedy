# Automation Scripts

This directory contains Python automation scripts for repository management tasks using the [Plumbum](https://plumbum.readthedocs.io/) library for command execution.

## Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Scripts

### post_merge_cleanup.py

Automates cleanup of consolidated PRs and their branches after a consolidation PR has been merged.

**Usage:**
```bash
# Basic usage
python scripts/post_merge_cleanup.py --pr-number 18

# Dry run (no actual changes)
python scripts/post_merge_cleanup.py --pr-number 18 --dry-run

# Custom PR numbers and branches
python scripts/post_merge_cleanup.py --pr-number 18 \
  --pr-numbers-to-close 1 7 8 \
  --branches-to-delete feature/old-1 feature/old-2
```

**Required Environment Variables:**
- `GITHUB_TOKEN`: GitHub personal access token with `repo` permissions
- `GITHUB_REPOSITORY`: Repository in format "owner/repo" (auto-detected from git remote if not set)

**Features:**
- Closes consolidated PRs with explanatory comments
- Deletes obsolete branches
- Adds cleanup summary comment to consolidation PR
- Supports dry-run mode for safe testing

### branch_manager.py

Comprehensive branch management tool for listing, cleaning up, protecting, and syncing branches.

**Commands:**

#### List Branches
```bash
# List all branches
python scripts/branch_manager.py list

# List branches older than 90 days
python scripts/branch_manager.py list --older-than 90

# List branches matching a pattern
python scripts/branch_manager.py list --pattern "feature/"
```

#### Cleanup Stale Branches
```bash
# Delete branches older than 180 days
python scripts/branch_manager.py cleanup --older-than 180

# Dry run with custom exclusions
python scripts/branch_manager.py cleanup --older-than 180 \
  --exclude master main develop staging \
  --dry-run

# Cleanup only specific pattern
python scripts/branch_manager.py cleanup --older-than 90 \
  --pattern "snyk-"
```

#### Protect Branch
```bash
# Protect master branch with default settings
python scripts/branch_manager.py protect --branch master

# Custom protection rules
python scripts/branch_manager.py protect --branch develop \
  --require-reviews 2 \
  --require-ci
```

#### Sync Branch
```bash
# Sync feature branch with master
python scripts/branch_manager.py sync --branch feature/my-feature --upstream master

# Dry run
python scripts/branch_manager.py sync --branch feature/my-feature --dry-run
```

**Required Environment Variables:**
- `GITHUB_TOKEN`: GitHub personal access token with `repo` permissions
- `GITHUB_REPOSITORY`: Repository in format "owner/repo" (auto-detected if not set)

## Integration with GitHub Actions

These scripts are designed to be used in GitHub Actions workflows. See the workflows in `.github/workflows/` for examples.

Example workflow usage:
```yaml
- name: Run post-merge cleanup
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITHUB_REPOSITORY: ${{ github.repository }}
  run: |
    pip install -r automation/requirements.txt
    python automation/scripts/post_merge_cleanup.py --pr-number ${{ github.event.pull_request.number }}
```

## Development

### Testing Scripts Locally

Always use `--dry-run` flag when testing:

```bash
# Test post-merge cleanup
export GITHUB_TOKEN="your-token"
export GITHUB_REPOSITORY="owner/repo"
python scripts/post_merge_cleanup.py --pr-number 18 --dry-run

# Test branch cleanup
python scripts/branch_manager.py cleanup --older-than 180 --dry-run
```

### Adding New Scripts

1. Create a new Python script in `scripts/`
2. Add shebang and proper documentation
3. Add required dependencies to `requirements.txt`
4. Make script executable: `chmod +x scripts/your_script.py`
5. Update this README with usage instructions
6. Create corresponding GitHub Actions workflow if needed

## Best Practices

- **Always test with `--dry-run` first** before running scripts that modify repository state
- Use descriptive commit messages when adding new scripts
- Document all environment variables and parameters
- Handle errors gracefully with informative messages
- Use Plumbum for command execution instead of `subprocess`
- Follow PEP 8 style guidelines
- Add type hints for better code maintainability

## Troubleshooting

### "GITHUB_TOKEN environment variable not set"
Set your GitHub token:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### "Could not determine repository name"
Set the repository explicitly:
```bash
export GITHUB_REPOSITORY="owner/repo"
```

### Permission Denied Errors
Ensure your GitHub token has `repo` scope permissions.

### Branch Not Found Errors
The branch may have already been deleted. Check branch existence with:
```bash
python scripts/branch_manager.py list
```
