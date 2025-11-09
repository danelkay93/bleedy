# DevContainer and Automation Guide

**Single Source of Truth for DevOps, CI/CD, and Automation**

This document consolidates all DevOps, CI/CD, infrastructure, and automation information for the Bleedy project into a single, comprehensive guide.

## Table of Contents

1. [Overview](#overview)
2. [Development Environment](#development-environment)
3. [CI/CD Pipeline](#cicd-pipeline)
4. [Infrastructure as Code](#infrastructure-as-code)
5. [Automation](#automation)
6. [Workflows Reference](#workflows-reference)
7. [Maintenance and Operations](#maintenance-and-operations)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Overview

### Architecture

The Bleedy project uses a modern DevOps stack with:

- **Docker-based CI/CD**: Primary build and test pipeline
- **Python Automation**: Branch and environment management
- **Infrastructure as Code**: Pulumi for Azure resources
- **GitHub Actions**: Automated workflows for all operations

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Actions                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Docker CI   │  │   Branch     │  │   Pulumi     │ │
│  │  (Primary)   │  │  Management  │  │     IaC      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Quick CI    │  │   Security   │  │  SonarCloud  │ │
│  │  (Checks)    │  │    Scan      │  │   Analysis   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │    Azure     │  │   Lock File  │                    │
│  │  Deployment  │  │     Sync     │                    │
│  └──────────────┘  └──────────────┘                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Development Environment

### Local Setup

#### Prerequisites

- **Node.js**: 20.x or later (matches @tsconfig/node20)
- **npm**: 11.0.0+ (required for proper patch application)
- **Python**: 3.8+ (for automation scripts)
- **GitHub CLI**: Latest version (for automation)
- **Docker**: Latest version (optional, for Docker-based development)

#### Quick Start

```bash
# Clone the repository
git clone https://github.com/danelkay93/bleedy.git
cd bleedy

# Install dependencies
npm install

# Start development server
npm run dev

# In another terminal, verify build
npm run build
```

#### Verification Steps

```bash
# Check formatting
npm run format:check

# Lint code
npm run lint

# Type check (may have known non-blocking errors)
npm run type-check

# Build project
npm run build

# Validate lock file
bash scripts/validate-lockfile.sh
```

### Development Container

A complete devcontainer configuration is available in `.devcontainer/` providing:

- **Consistent development environment** - Docker-based reproducible setup
- **Pre-configured tools** - Node.js 20, Python 3, GitHub CLI, Docker-in-Docker
- **Automated setup** - Post-creation script installs dependencies and configures git
- **VS Code integration** - Recommended extensions and settings
- **Multi-agent support** - Optimized for Claude Code, Copilot, CodeRabbit collaboration

**Quick Start**:
```bash
# Open in VS Code Dev Container
code .
# Click "Reopen in Container" when prompted

# Or use Docker directly
docker build -t bleedy-dev -f .devcontainer/Dockerfile .
docker run -it -v $(pwd):/workspace -p 5173:5173 bleedy-dev
```

See `.devcontainer/README.md` for complete documentation.

---

## CI/CD Pipeline

### Pipeline Flow

1. **Quick CI** (`ci.yml`) - Fast preliminary checks
   - Lock file validation
   - Basic file checks
   - Quick validation

2. **Docker CI** (`docker-compose.yml`) - **PRIMARY CI**
   - Lock file validation (integrated)
   - Dependency installation with retry
   - Code formatting check
   - Linting
   - Type checking
   - Build verification
   - Security scanning

3. **Specialized Workflows**
   - SonarCloud analysis
   - Azure deployment
   - Lock file synchronization

### Docker-Based CI (Primary)

The Docker CI workflow is the **single source of truth** for comprehensive CI checks.

**Location**: `.github/workflows/docker-compose.yml`

**Features**:

- Integrated lock file validation
- Retry mechanism for npm ci (3 attempts)
- Comprehensive code quality checks
- Security vulnerability scanning
- Build artifact upload

**Triggers**:

- Push to master
- Pull requests
- Manual dispatch

**Jobs**:

1. **docker-ci**: Main build and validation
   - Validates package-lock.json
   - Installs dependencies
   - Runs format, lint, type-check
   - Builds project
   - Uploads build artifacts

2. **docker-security-scan**: Security analysis
   - Runs npm audit
   - Fails on critical/high vulnerabilities
   - Uploads audit results

### Lock File Management

**Script**: `scripts/validate-lockfile.sh`

Validates that `package-lock.json` is in sync with `package.json`.

**Features**:

- Checks lock file exists and is valid JSON
- Verifies lock file version
- Performs dry-run install check
- Provides actionable error messages

**Usage**:

```bash
# Validate manually
bash scripts/validate-lockfile.sh

# Fix out-of-sync lock file
rm package-lock.json
npm install
git add package-lock.json
git commit -m "chore: regenerate package-lock.json"
```

**Automatic Sync**:
The `lockfile-sync.yml` workflow automatically:

- Detects out-of-sync lock files on PRs
- Regenerates lock file if needed
- Commits and pushes changes
- Adds explanatory PR comment

### Build Configuration

#### Node.js Version

- Primary: **20.x**
- Specified in all workflows
- Matches `@tsconfig/node20` configuration

#### Caching Strategy

- npm cache enabled in all workflows
- Improves build times by ~30-50%
- Cache key based on `package-lock.json`

#### Retry Mechanism

All workflows use retry logic for `npm ci`:

- Maximum 3 attempts
- 30-second delay between attempts
- Cache cleaning on retry
- Detailed error messages

---

## Infrastructure as Code

### Pulumi Configuration

**Location**: `infrastructure/` directory

**Workflow**: `.github/workflows/pulumi.yml`

**Purpose**: Manage Azure infrastructure using Pulumi IaC

**Status**: Infrastructure directory prepared, workflow in place, awaiting infrastructure code

### Workflow Behavior

**On Pull Requests**:

- Runs `pulumi preview` to show planned changes
- Does not apply changes
- Provides visibility into infrastructure modifications

**On Master Push**:

- Runs `pulumi up --yes` to apply changes
- Exports stack output
- Uploads output as artifact

### Setup Instructions

```bash
# Install Pulumi CLI
curl -fsSL https://get.pulumi.com | sh

# Login to Pulumi
pulumi login

# Initialize project (when ready)
cd infrastructure
pulumi new azure-python  # or azure-typescript

# Configure stack
pulumi config set azure-native:location EastUS
```

### Planned Resources

- Azure Static Web Apps configuration
- Azure Storage for artifacts
- Azure CDN configuration
- Monitoring and alerting resources
- DNS and domain configuration

### Security

- `PULUMI_ACCESS_TOKEN`: Stored in GitHub Secrets
- Azure credentials: Configured in Pulumi config
- Sensitive values: Encrypted using Pulumi secrets

---

## Automation

### Branch Management

**Script**: `automation/branch_manager.py`

**Purpose**: Automated branch and Azure staging environment management

**Features**:

- Branch lifecycle management
- Stale branch detection
- Azure Static Web App staging cleanup
- PR-based environment tracking
- GitHub CLI integration

**Usage**:

```bash
# Status check
python3 automation/branch_manager.py --action status

# Find stale branches
python3 automation/branch_manager.py --action branches

# Check staging environments
python3 automation/branch_manager.py --action staging

# Full cleanup (dry run)
python3 automation/branch_manager.py --dry-run

# Full cleanup (actual)
python3 automation/branch_manager.py
```

**GitHub Actions Integration**:

- Workflow: `.github/workflows/branch-management.yml`
- Schedule: Weekly on Sundays at 3 AM UTC
- Manual trigger: Available via workflow_dispatch

### Staging Environment Management

**Problem Addressed**:
Azure Static Web Apps free tier has a limit of 10 staging environments (one per PR).

**Solution**:
The branch manager:

- Tracks open PRs and their staging environments
- Identifies orphaned environments from closed PRs
- Creates alerts when approaching limits
- Provides visibility into active environments

**Alert Thresholds**:

- **Warning**: 7+ active staging environments
- **Critical**: 9+ active staging environments

**Best Practices**:

- Keep concurrent open PRs ≤ 8
- Close or merge PRs promptly
- Use draft PRs for work-in-progress
- Run branch management workflow before opening new PRs

### Deprecated Workflows

**`azure-staging-cleanup.yml`**: DEPRECATED

- Replaced by `branch-management.yml`
- Scheduled execution disabled
- Manual trigger still available (but not recommended)
- Will be removed in future update

**Reason for Deprecation**:
The Python-based `branch_manager.py` provides:

- More comprehensive tracking
- Better integration with GitHub CLI
- Single script for multiple automation tasks
- Easier maintenance and extension

---

## Workflows Reference

### Active Workflows

| Workflow                      | Purpose                                | Trigger                  | Status                  |
| ----------------------------- | -------------------------------------- | ------------------------ | ----------------------- |
| `docker-compose.yml`          | **Primary CI** - Build, test, security | Push, PR                 | ✅ Active (Primary)     |
| `ci.yml`                      | Quick validation checks                | Push, PR                 | ✅ Active (Lightweight) |
| `branch-management.yml`       | Branch and environment automation      | Weekly, Manual           | ✅ Active               |
| `pulumi.yml`                  | Infrastructure as Code                 | Push (infra changes), PR | ✅ Active               |
| `lockfile-sync.yml`           | Lock file synchronization              | PR (package changes)     | ✅ Active               |
| `azure-static-web-apps-*.yml` | Azure deployment                       | Push, PR                 | ✅ Active               |
| `sonarcloud.yml`              | Code quality analysis                  | Push, PR                 | ✅ Active               |
| `post-merge-cleanup.yml`      | Post-merge automation                  | PR merge                 | ✅ Active               |

### Deprecated Workflows

| Workflow                    | Replaced By             | Status        |
| --------------------------- | ----------------------- | ------------- |
| `azure-staging-cleanup.yml` | `branch-management.yml` | ⚠️ Deprecated |

### Workflow Relationships

```
Quick CI (ci.yml)
    ↓
Docker CI (docker-compose.yml) ← Primary CI
    ↓
SonarCloud Analysis
    ↓
Azure Deployment
```

---

## Maintenance and Operations

### Regular Tasks

#### Daily

- Monitor workflow runs for failures
- Review security alerts

#### Weekly

- Review and merge Dependabot PRs
- Check branch management summary
- Monitor staging environment usage

#### Monthly

- Update dependencies: `npm update`
- Review and address moderate security vulnerabilities
- Check for outdated GitHub Actions versions
- Review and optimize build performance

#### Quarterly

- Major dependency updates (Vue, Vite, etc.)
- Review and update workflow configurations
- Audit and clean up unused workflows
- Update documentation

### Monitoring

#### Key Metrics

| Metric                   | Target          | Current            |
| ------------------------ | --------------- | ------------------ |
| Build Success Rate       | > 95%           | Monitor            |
| Average Build Time       | < 10 minutes    | ~7-8s (build only) |
| Deployment Success Rate  | > 98%           | Monitor            |
| Security Vulnerabilities | 0 critical/high | 5 moderate         |

#### Alerts to Configure

- Multiple consecutive build failures
- Security vulnerabilities detected
- Staging environment limit approaching
- Deployment failures

### Dependency Management

#### Dependabot Configuration

- **npm dependencies**: Weekly updates on Mondays
- **GitHub Actions**: Monthly updates
- Groups related dependencies
- Limits open PRs to 5 (npm) and 3 (Actions)

#### Ignored Major Updates

Major version updates require manual review:

- `vue`
- `element-plus`
- `vite`

#### Security Updates

```bash
# Run audit locally
npm audit

# Fix automatically fixable issues
npm audit fix

# Fix with breaking changes (caution!)
npm audit fix --force
```

### Pre-commit Hooks (Planned)

#### Current Status

- Husky v9.1.7 installed but hooks not configured
- `.huskyrc.json` exists (legacy format, not used by Husky v9)

#### Planned Hooks

**Pre-commit**:

```bash
npm run format:check
npm run lint -- --no-fix
```

**Pre-push**:

```bash
npm run type-check
npm run build
```

#### Setup Instructions

```bash
# Initialize Husky v9
npx husky init

# Create pre-commit hook
echo "npm run format:check && npm run lint -- --no-fix" > .husky/pre-commit
chmod +x .husky/pre-commit

# Create pre-push hook
echo "npm run type-check && npm run build" > .husky/pre-push
chmod +x .husky/pre-push
```

---

## Troubleshooting

### Common Issues

#### Build Failures

**Symptoms**:

- TypeScript errors
- Missing dependencies
- Import resolution failures

**Solutions**:

1. Pull latest changes: `git pull`
2. Clean install: `rm -rf node_modules && npm install`
3. Verify patches applied: Check for `patches/` directory
4. Build locally: `npm run build`

#### npm ci Failures

**Symptoms**:

- "ENOLOCK: no package-lock.json found"
- "Invalid package-lock.json"
- Network timeout errors

**Solutions**:

1. Let retry mechanism complete (automatic in CI)
2. If persistent, regenerate lock file locally:
   ```bash
   rm package-lock.json
   npm install
   git add package-lock.json
   git commit -m "chore: regenerate package-lock.json"
   ```

#### Lock File Out of Sync

**Symptoms**:

- `lockfile-sync` workflow creates commits
- npm ci fails with hash mismatch

**Solutions**:

- **Automatic**: Workflow fixes and commits changes
- **Manual prevention**: Always commit lock file with package.json
- **Verification**: Run `bash scripts/validate-lockfile.sh`

#### Deployment Failures

**Symptoms**:

- Azure deployment timeout
- "Staging limit reached" error
- Build output validation failure

**Solutions**:

1. Check staging environment count
   ```bash
   python3 automation/branch_manager.py --action staging
   ```
2. Verify `dist/` directory exists and contains `index.html`
3. Review Azure Static Web Apps logs
4. Run branch management workflow to clean up

#### Staging Environment Limit

**Symptoms**:

- Cannot create new PR staging environment
- "Staging limit reached" message

**Solutions**:

1. Check current usage:
   ```bash
   python3 automation/branch_manager.py --action status
   ```
2. Close or merge stale PRs
3. Run cleanup workflow:
   - Actions → Branch Management → Run workflow
   - Select action: `staging`
   - Dry run: `false`

#### Security Audit Failures

**Symptoms**:

- CI fails on security-audit job
- Critical/high severity vulnerabilities found

**Solutions**:

1. Review vulnerability details in workflow logs
2. Check for available patches: `npm audit fix`
3. Update vulnerable dependencies
4. If no fix available, document and create issue
5. Consider temporary exception if risk is low

### Debug Mode

Enable detailed logging in workflows:

```yaml
- name: Enable debug logging
  run: |
    echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
    echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV
```

### Getting Help

1. Check this documentation
2. Review workflow run logs in GitHub Actions
3. Check existing GitHub Issues
4. Create new issue with:
   - Workflow run link
   - Error messages
   - Steps to reproduce
   - Environment details

---

## Best Practices

### Package Management

#### DO ✅

- Always run `npm install` after pulling changes
- Commit `package-lock.json` with `package.json` updates
- Use `npm ci` in CI/CD pipelines (faster and more reliable)
- Let automated workflow fix sync issues
- Run lock file validation before committing

#### DON'T ❌

- Never manually edit `package-lock.json`
- Don't ignore lock file changes in git
- Don't use `npm install` in CI/CD pipelines
- Don't commit with out-of-sync lock files
- Don't delete lock file unless regenerating

### Git Workflow

#### Branch Naming

- Features: `feat/description`
- Bug fixes: `fix/description`
- Refactoring: `refactor/description`
- Documentation: `docs/description`
- CI/CD: `ci/description`
- Infrastructure: `infra/description`

#### Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

### PR Management

#### Before Opening PR

1. Ensure lock file is in sync
2. Run local validation:
   ```bash
   npm run format:check
   npm run lint
   npm run build
   ```
3. Check staging environment count
4. Review changes for large files or secrets

#### During PR Review

- Address review comments promptly
- Keep PR focused and small
- Update tests if applicable
- Monitor CI checks

#### After PR Merge

- Delete branch (automatic via post-merge cleanup)
- Verify staging environment cleanup
- Monitor production deployment

### Security

#### Vulnerability Management

1. **Critical/High Severity**: Address immediately
   - Review details
   - Update affected package
   - Test thoroughly
   - Monitor for patches if no fix available

2. **Moderate Severity**: Address in next sprint
   - Evaluate risk vs. effort
   - Plan update in regular cycle
   - Consider workarounds if needed

3. **Low Severity**: Address in maintenance cycle
   - Monitor for severity changes
   - Include in bulk updates
   - Document known issues

#### Secrets Management

- Never commit secrets to repository
- Use GitHub Secrets for CI/CD
- Use Pulumi secrets for infrastructure
- Rotate secrets regularly
- Audit secret usage quarterly

### Performance

#### Build Optimization

```typescript
// vite.config.ts - Manual chunk splitting
build: {
  chunkSizeWarningLimit: 1000,
  rollupOptions: {
    output: {
      manualChunks: {
        'vendor-vue': ['vue', 'vue-router', 'pinia'],
        'vendor-ui': ['element-plus', '@element-plus/icons-vue'],
        'vendor-utils': ['file-saver', 'jszip'],
        'vendor-sketchy': ['roughjs', 'wired-elements']
      }
    }
  }
}
```

**Guidelines**:

- Keep vendor chunks separate from application code
- Group related libraries
- Monitor chunk sizes after adding dependencies
- Adjust warning limit only when justified

---

## Additional Resources

### Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [npm Documentation](https://docs.npmjs.com/)
- [Vite Build Documentation](https://vitejs.dev/guide/build.html)

### Project Documentation

- `README.md` - Project overview
- `.github/copilot-instructions.md` - Development guidelines
- `.github/AGENT_COLLABORATION.md` - Multi-agent collaboration
- `automation/README.md` - Automation scripts
- `infrastructure/README.md` - IaC details

### Tools

- [GitHub CLI](https://cli.github.com/)
- [Pulumi CLI](https://www.pulumi.com/docs/install/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

---

## Change Log

### Version 1.0.0 (October 2025)

**Created**: Initial consolidated documentation

**Consolidated from**:

- CI/CD guide and quick reference
- Implementation checklist
- Automation setup guide
- Various workflow documentation

**New Features Documented**:

- Docker-based CI as primary CI
- Python automation with branch_manager.py
- Pulumi IaC workflow
- Lock file validation integration
- Deprecated azure-staging-cleanup workflow

---

**Document Version**: 1.0.0  
**Last Updated**: October 20, 2025  
**Maintained By**: Development Team  
**Status**: Active - Single Source of Truth
