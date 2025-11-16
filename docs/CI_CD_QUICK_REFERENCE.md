# CI/CD Quick Reference

Quick reference guide for common CI/CD tasks and commands.

## Daily Operations

### Check Build Status
```bash
# View in GitHub
# Navigate to: https://github.com/danelkay93/bleedy/actions

# Or use GitHub CLI
gh run list --limit 5
gh run view <run-id>
```

### Run Security Audit Locally
```bash
npm audit

# Fix automatically fixable issues
npm audit fix

# View detailed report
npm audit --json > audit-report.json
```

### Test Build Locally
```bash
# Clean build
rm -rf dist node_modules
npm install
npm run build

# Check bundle sizes
ls -lh dist/assets/
```

## Workflow Management

### Trigger Manual Workflows

#### Lock File Sync
```bash
gh workflow run lockfile-sync.yml
```

#### Azure Staging Cleanup
```bash
gh workflow run azure-staging-cleanup.yml --field dry_run=true
```

### View Workflow Logs
```bash
# List recent runs
gh run list --workflow=ci.yml --limit 5

# View specific run
gh run view <run-id> --log

# Download logs
gh run download <run-id>
```

## Common Tasks

### Update Dependencies
```bash
# Check for updates
npm outdated

# Update all to latest compatible
npm update

# Update specific package
npm update <package-name>

# Always commit package-lock.json
git add package.json package-lock.json
git commit -m "chore: update dependencies"
```

### Fix Lock File Issues
```bash
# If out of sync
rm package-lock.json
npm install
git add package-lock.json
git commit -m "chore: regenerate package-lock.json"

# Or let the workflow handle it automatically
```

### Resolve Build Failures

#### TypeScript Errors
```bash
npm run type-check
# Fix reported errors in code
```

#### ESLint Errors
```bash
npm run lint
# Fix reported errors
```

#### Format Issues
```bash
npm run format
git add .
git commit -m "chore: format code"
```

### Test Vite Configuration Changes
```bash
# Development build
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

## Deployment

### Check Azure Deployment Status
```bash
# Via GitHub Actions
gh run list --workflow=azure-static-web-apps-*.yml --limit 5

# Check PR deployment comments
gh pr view <pr-number>
```

### Force Redeploy
```bash
# Push an empty commit
git commit --allow-empty -m "chore: trigger deployment"
git push
```

## Troubleshooting

### CI Failing with npm ci Error
```bash
# Check if lock file is out of sync
npm ci --dry-run

# If fails, regenerate
rm package-lock.json
npm install

# Workflow will retry automatically (3 attempts)
```

### Build Failing Locally but Passing in CI
```bash
# Use exact Node version from CI
nvm install 20
nvm use 20

# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Deployment Failing
```bash
# Check staging environment count
# Via GitHub: Actions → Azure Staging Cleanup → Run workflow (dry_run=true)

# Or manually check open PRs
gh pr list --state open
```

### Security Audit Blocking Merge
```bash
# Review vulnerabilities
npm audit

# Update vulnerable packages
npm update <vulnerable-package>

# If no fix available, check if dev dependency
# Consider --production flag for runtime-only audit
npm audit --production
```

## Monitoring

### Check Workflow Success Rate
```bash
gh run list --workflow=ci.yml --limit 20 --json conclusion
```

### View Build Performance
```bash
# Check recent build times
gh run list --workflow=ci.yml --limit 10 --json conclusion,timing
```

### Monitor Open PRs and Staging Environments
```bash
gh pr list --state open
```

## Emergency Procedures

### Disable a Workflow Temporarily
1. Edit workflow file
2. Add `if: false` to job:
```yaml
jobs:
  my-job:
    if: false  # Temporarily disabled
```
3. Commit and push

### Rollback a Bad Deployment
```bash
# Revert to previous commit
git revert HEAD
git push

# Or force push to previous state (use with caution)
git reset --hard <previous-commit>
git push --force
```

### Skip CI on Commit
```bash
git commit -m "docs: update README [skip ci]"
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# CI/CD shortcuts
alias ci-status='gh run list --limit 5'
alias ci-logs='gh run view --log'
alias ci-build='npm run build'
alias ci-audit='npm audit'
alias ci-fix='npm audit fix && npm run lint && npm run format'
```

## GitHub CLI Setup

If you don't have GitHub CLI:

```bash
# macOS
brew install gh

# Linux
curl -sS https://webi.sh/gh | sh

# Windows
winget install GitHub.cli

# Authenticate
gh auth login
```

## Links

- [Main CI/CD Guide](./CI_CD_GUIDE.md)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Azure Static Web Apps](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [npm CLI Docs](https://docs.npmjs.com/cli/)
- [Vite Build Docs](https://vitejs.dev/guide/build.html)

---

**Last Updated:** 2025-10-16
**Version:** 1.0.0
