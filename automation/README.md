# Automation Scripts

This directory contains automation scripts for managing the Bleedy project infrastructure and workflows.

## Scripts

### `branch_manager.py`

Python script for automated branch and environment management.

**Features:**

- Branch lifecycle management (creation, deletion, stale detection)
- Azure Static Web App staging environment cleanup
- PR-based staging environment tracking
- Integrated with GitHub CLI for seamless operation

**Usage:**

```bash
# Run full cleanup (dry run)
python3 automation/branch_manager.py --dry-run

# Run actual cleanup
python3 automation/branch_manager.py

# Check status only
python3 automation/branch_manager.py --action status

# Find stale branches
python3 automation/branch_manager.py --action branches

# Check staging environments
python3 automation/branch_manager.py --action staging
```

**Requirements:**

- Python 3.8+
- GitHub CLI (`gh`) installed and authenticated

**GitHub Actions Integration:**

This script is integrated with the `branch-management.yml` workflow that runs:

- Weekly on Sundays at 3 AM UTC (automated)
- On-demand via workflow_dispatch

## Configuration

The scripts use environment variables and GitHub CLI authentication:

- `GH_TOKEN`: GitHub token for API access (automatically provided in Actions)
- Repository owner and name can be specified via command-line arguments

## Development

To test locally:

```bash
# Authenticate GitHub CLI
gh auth login

# Run in dry-run mode
python3 automation/branch_manager.py --dry-run --action status
```

## Workflow Integration

These automation scripts replace manual workflows:

- Replaces: `.github/workflows/azure-staging-cleanup.yml`
- Provides: More comprehensive branch and environment management
- Benefits: Single script for multiple automation tasks

## Future Enhancements

- Automatic PR labeling based on branch age
- Integration with Azure API for direct environment management
- Notification system for approaching limits
- Branch protection rule management
