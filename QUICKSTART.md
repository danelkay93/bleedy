# Quick Start Guide - Infrastructure and Automation

This guide helps you quickly get started with the new infrastructure and automation features added to the Bleedy project.

## What's New?

This PR adds:
- 🏗️ **Infrastructure as Code** with Pulumi
- 🤖 **Automation Scripts** for repository management
- 🐳 **Docker** containerization
- ⚙️ **Enhanced GitHub Actions** workflows
- 📊 **Monitoring** strategy documentation

## Quick Setup

### 1. Application Development (No Changes)

Normal development workflow remains unchanged:

```bash
npm install
npm run dev
```

### 2. Using Docker (Optional)

#### Development Mode
```bash
docker-compose up web
```
Access at: http://localhost:5173

#### Production Mode
```bash
docker-compose build
docker-compose --profile production up nginx
```
Access at: http://localhost:8080

### 3. Automation Scripts (For Maintainers)

#### List All Branches
```bash
cd automation
pip install -r requirements.txt
python scripts/branch_manager.py list
```

#### Cleanup Stale Branches (Dry Run)
```bash
export GITHUB_TOKEN="your-token"
export GITHUB_REPOSITORY="danelkay93/bleedy"
python scripts/branch_manager.py cleanup --older-than 180 --dry-run
```

#### Post-Merge Cleanup (Dry Run)
```bash
python scripts/post_merge_cleanup.py --pr-number 18 --dry-run
```

### 4. Infrastructure Management (Optional)

Only needed if managing infrastructure:

```bash
# Install Pulumi
curl -fsSL https://get.pulumi.com | sh

# Setup
cd infrastructure
pip install -r requirements.txt
pulumi login

# Preview changes
pulumi preview

# Apply changes (requires PULUMI_ACCESS_TOKEN)
pulumi up
```

## GitHub Actions Workflows

### Automatic Workflows

These run automatically:

1. **CI Checks** (`ci.yml`)
   - Runs on every push and PR
   - Checks formatting, linting, types, and builds

2. **Docker Compose** (`docker-compose.yml`)
   - Runs on Dockerfile changes
   - Builds and tests containers
   - Security scans with Trivy

3. **Post-Merge Cleanup** (`post-merge-cleanup.yml`)
   - Runs when consolidation PRs are merged
   - Closes old PRs and deletes branches

4. **Branch Management** (`branch-management.yml`)
   - Runs weekly
   - Reports stale branches

### Manual Workflows

Trigger manually from GitHub Actions tab:

1. **Pulumi** (`pulumi.yml`)
   - Deploy infrastructure changes
   - Requires `PULUMI_ACCESS_TOKEN` secret

2. **Branch Management** (`branch-management.yml`)
   - List, cleanup, or protect branches
   - Always use dry-run first!

## Directory Structure

```
bleedy/
├── automation/              # 🤖 Automation scripts
│   ├── scripts/
│   │   ├── post_merge_cleanup.py
│   │   └── branch_manager.py
│   └── requirements.txt
│
├── infrastructure/          # 🏗️ Pulumi IaC
│   ├── __main__.py
│   ├── Pulumi.yaml
│   └── requirements.txt
│
├── .github/workflows/       # ⚙️ GitHub Actions
│   ├── ci.yml
│   ├── pulumi.yml
│   ├── docker-compose.yml
│   ├── branch-management.yml
│   └── post-merge-cleanup.yml
│
├── Dockerfile              # 🐳 Container build
├── docker-compose.yml      # 🐳 Service orchestration
├── nginx.conf             # 🌐 Production web server
│
└── Documentation
    ├── INFRASTRUCTURE.md   # Complete infrastructure guide
    ├── MONITORING.md      # Monitoring strategy
    └── automation/README.md  # Automation scripts guide
```

## Common Tasks

### For Developers

**Normal development** - Nothing changes:
```bash
npm install
npm run dev
npm run build
```

**Test with Docker** - Optional:
```bash
docker-compose up web
```

### For Maintainers

**List branches**:
```bash
cd automation
pip install -r requirements.txt
python scripts/branch_manager.py list
```

**Cleanup old branches** (always dry-run first):
```bash
export GITHUB_TOKEN="your-token"
python scripts/branch_manager.py cleanup --older-than 180 --dry-run
```

**Protect important branches**:
```bash
python scripts/branch_manager.py protect --branch master --dry-run
```

### For DevOps

**Deploy infrastructure**:
```bash
cd infrastructure
pulumi preview  # Always preview first
pulumi up       # Apply changes
```

**Check infrastructure status**:
```bash
pulumi stack output
pulumi stack
```

## What Needs Configuration?

### Minimal Setup (Everything Works)
- Nothing! The PR works out of the box for normal development.

### Optional Features

#### For Pulumi (Infrastructure Management)
1. Create account at [app.pulumi.com](https://app.pulumi.com)
2. Get access token
3. Add `PULUMI_ACCESS_TOKEN` to GitHub secrets
4. Run `pulumi login` locally

#### For Automation Scripts
1. Generate GitHub personal access token with `repo` scope
2. Set environment variables:
   ```bash
   export GITHUB_TOKEN="your-token"
   export GITHUB_REPOSITORY="danelkay93/bleedy"
   ```

#### For Monitoring (Future)
See `MONITORING.md` for tool recommendations.

## Testing Your Changes

### Test Build
```bash
npm run build
```

### Test Python Scripts
```bash
python3 -m py_compile automation/scripts/*.py
```

### Test Docker
```bash
docker-compose build
docker-compose up web
```

### Test Workflows (Locally)
```bash
# Install act (https://github.com/nektos/act)
act -l  # List workflows
act pull_request  # Simulate PR event
```

## Need Help?

### Documentation
- **Complete infrastructure guide**: [INFRASTRUCTURE.md](INFRASTRUCTURE.md)
- **Monitoring strategy**: [MONITORING.md](MONITORING.md)
- **Automation scripts**: [automation/README.md](automation/README.md)
- **Pulumi setup**: [infrastructure/README.md](infrastructure/README.md)

### Troubleshooting
- Check GitHub Actions logs for workflow issues
- Use `--dry-run` flag for all automation scripts
- Review Docker logs: `docker-compose logs`
- Check Pulumi state: `pulumi stack`

### Questions?
- Open an issue in the repository
- Review documentation in respective directories
- Check tool-specific documentation

## What's Next?

After merging this PR:

1. **Optional**: Set up Pulumi for infrastructure management
2. **Optional**: Configure monitoring (see `MONITORING.md`)
3. **Recommended**: Review automation scripts locally
4. **Recommended**: Test Docker setup locally
5. Continue normal development!

---

**Remember**: All new features are optional and don't affect normal development workflow!
