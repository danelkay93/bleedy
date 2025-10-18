# Automation Setup Guide

This document explains the automated workflows and configurations set up for the Bleedy project to handle post-merge actions, dependency management, and code quality checks.

## 🤖 Automated Workflows

### 1. Post-Merge Cleanup (`post-merge-cleanup.yml`)

**Purpose**: Automatically clean up consolidated PRs and branches after a consolidation PR is merged.

**Trigger**: Runs when a PR is merged to `master` or `main`

**Actions Performed**:

- ✅ Detects if the merged PR is a consolidation PR (checks title/description)
- ✅ Closes all consolidated PRs (PRs #1, #7, #8, #10, #12, #14, #15)
- ✅ Adds explanatory comments to closed PRs
- ✅ Deletes obsolete branches:
  - `refactor-cleanup`
  - `phase1-refactor-pyscript-deps`
  - `fix/eslint-errors`
  - `snyk-upgrade-element-plus-*` branches
- ✅ Posts summary comment on the merged PR

**Configuration**: `.github/workflows/post-merge-cleanup.yml`

**Requirements**:

- GitHub token with appropriate permissions (automatically provided by GitHub Actions)
- No manual intervention needed

**How it works**:

1. When any PR is merged to master, the workflow checks if it's a consolidation PR
2. If yes, it iterates through the list of consolidated PR numbers and branch names
3. Closes each PR with a comment explaining the consolidation
4. Deletes each branch that was consolidated
5. Posts a summary comment

### 2. CI Checks and Build (`ci.yml`)

**Purpose**: Validate code quality, formatting, type safety, and build success on every PR.

**Trigger**:

- Push to `master`
- Pull request opened, synchronized, or reopened

**Actions Performed**:

- ✅ Checks code formatting with Prettier
- ✅ Lints code with ESLint (no auto-fix in CI)
- ✅ Runs TypeScript type checking
- ✅ Builds the project

**Configuration**: `.github/workflows/ci.yml`

### 3. Dependabot (`dependabot.yml`)

**Purpose**: Automatically monitor and update dependencies to keep the project secure and up-to-date.

**Schedule**:

- **npm dependencies**: Weekly on Mondays at 09:00 UTC
- **GitHub Actions**: Monthly

**Features**:

- 📦 Groups related dependencies to reduce PR noise
  - Production dependencies (Vue, Element Plus)
  - Development dependencies (TypeScript, ESLint, Vite)
- 🏷️ Applies labels: `dependencies`, `automated`
- 🚫 Ignores major version updates for critical dependencies
- 🔄 Automatically rebases PRs when needed
- 📊 Limits open PRs to 5 (npm) and 3 (GitHub Actions)

**Configuration**: `.github/dependabot.yml`

**Ignored Major Updates**:

- `vue` - Major updates require manual review
- `element-plus` - Major updates require manual review
- `vite` - Major updates require manual review

## 🪝 Pre-commit Hooks

### Husky Configuration

**Purpose**: Run code quality checks before commits and pushes to catch issues early.

**Configuration**: `.huskyrc.json`

**Hooks**:

#### Pre-commit

Runs before each commit:

```bash
npm run format:check  # Verify code formatting
npm run lint -- --no-fix  # Check for linting issues
```

#### Pre-push

Runs before pushing to remote:

```bash
npm run type-check  # Verify TypeScript types
npm run build  # Ensure project builds successfully
```

**Setup Instructions**:

1. Install Husky (if not already installed):

```bash
npm install --save-dev husky
```

2. Initialize Husky:

```bash
npx husky install
```

3. Add Husky setup to package.json (automatic with .huskyrc.json):

```json
{
  "scripts": {
    "prepare": "husky install"
  }
}
```

4. The hooks will automatically run based on `.huskyrc.json` configuration

### PyScript Version Check Hook

**Purpose**: Ensure PyScript version consistency across the codebase.

**Script**: `scripts/check-pyscript-version.sh`

**Status**: Placeholder implementation - needs completion

**To Integrate**:

1. Complete the version parsing logic in the script
2. Add to Husky pre-commit hook:

```bash
npx husky add .husky/pre-commit "bash scripts/check-pyscript-version.sh"
```

**Future Work**: See `TODO.md` for full implementation plan

## 🔐 Security Monitoring

### Current Setup

**Dependabot**: Enabled for automated security updates

- Monitors npm dependencies weekly
- Groups security updates with regular dependency updates
- Automatically opens PRs for vulnerabilities

### Recommended Additional Setup

**Snyk Integration** (Optional):

1. Sign up at https://snyk.io
2. Install Snyk GitHub App
3. Configure `.snyk` policy file if needed
4. Snyk will automatically:
   - Scan for vulnerabilities
   - Open PRs for fixes
   - Monitor continuously

**npm audit**:

- Run manually: `npm audit`
- Fix issues: `npm audit fix`
- For breaking changes: `npm audit fix --force` (review carefully)

## 🧭 Default Branch Visibility in Repository Snapshots

Some of our automation (and GitHub itself) assumes the repository snapshot
contains the canonical default branch. Before packaging the repo for local
automation or agent workspaces:

1. Run `git fetch origin --prune` to ensure the latest remote references are
   available locally.
2. Run `git remote set-head origin --auto` so that `origin/HEAD` points at the
   correct default branch (typically `main` or `master`).
3. Confirm the branch exists with `git branch -a | grep "origin/$(git rev-parse --abbrev-ref origin/HEAD | cut -d/ -f2)"`.

If @copilot is preparing the snapshot, ask it to include those commands in the
preparation flow. Should the default branch still be missing, rerun the steps
manually and regenerate the snapshot so subsequent agents can rely on a
complete history. The updated `branch_manager.py sync` command will use the
detected default branch automatically, but it still needs the reference to be
present locally.

## 📋 Manual Post-Merge Actions

Some actions cannot be fully automated and require manual intervention:

### Review Resolution

**To close open reviews on PR #18**:

1. Go to the PR page on GitHub
2. For each review, click "Dismiss review" if you have admin permissions
3. Or, ask reviewers to resolve their reviews after reading the responses

**Reviews to address**:

- CodeRabbit review (already addressed in commits)
- Any other pending reviews

### Deployment

After merge, deploy to production:

```bash
# Build production version
npm run build

# Deploy dist/ folder to your hosting service
# (e.g., Azure Static Web Apps, Netlify, Vercel)
```

### Security Vulnerabilities

Address the 5 moderate vulnerabilities mentioned:

```bash
# Review vulnerabilities
npm audit

# Fix automatically
npm audit fix

# If manual fixes needed, update specific packages
npm update <package-name>
```

## 🔄 Workflow Activation

### Immediate Actions (After This PR Merges)

1. **Post-merge cleanup**: Automatically runs
2. **Dependabot**: Starts monitoring (will open PRs starting next Monday)
3. **CI checks**: Already active

### Setup Required

1. **Husky hooks**: Run once by any developer:

```bash
npm install
npx husky install
```

2. **PyScript version check**: Complete script implementation (see TODO.md)

3. **Snyk** (optional): Configure through GitHub Apps

## 📊 Monitoring and Maintenance

### Weekly Tasks

- Review Dependabot PRs
- Merge approved dependency updates

### Monthly Tasks

- Review security audit: `npm audit`
- Check for outdated dependencies: `npm outdated`
- Review and update ignored major versions if needed

### Quarterly Tasks

- Review automation effectiveness
- Update workflow configurations if needed
- Review and update pre-commit hooks

## 🛠️ Customization

### Modifying PR/Branch Lists

To update the list of PRs/branches to clean up in future consolidations:

1. Edit `.github/workflows/post-merge-cleanup.yml`
2. Update arrays:
   - `prsToClose`: Add/remove PR numbers
   - `branchesToDelete`: Add/remove branch names

### Changing Dependabot Behavior

Edit `.github/dependabot.yml`:

- Adjust schedule frequency
- Modify grouping patterns
- Add/remove ignored dependencies
- Change PR limits

### Customizing Husky Hooks

Edit `.huskyrc.json`:

- Add new hooks (`commit-msg`, `post-merge`, etc.)
- Modify existing hook commands
- Add custom scripts

## 🐛 Troubleshooting

### Post-merge cleanup didn't run

**Possible causes**:

- PR title/description doesn't contain "consolidate"
- PR was closed but not merged
- Workflow permissions issue

**Solution**:

- Check workflow runs in GitHub Actions tab
- Manually close PRs and delete branches if needed

### Dependabot not creating PRs

**Possible causes**:

- Dependabot not enabled for repository
- No updates available
- Open PR limit reached

**Solution**:

- Check Dependabot status in repository settings
- Review Insights > Dependency graph > Dependabot

### Husky hooks not running

**Possible causes**:

- Husky not installed
- Git hooks not initialized
- Script execution permissions

**Solution**:

```bash
npm install
npx husky install
chmod +x .husky/*
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
- [Husky Documentation](https://typicode.github.io/husky/)
- [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit)

## 🎯 Future Enhancements

Potential improvements to automation (see FUTURE_WORK.md):

1. **Automated release notes generation**
2. **Automated changelog updates**
3. **Automated version bumping**
4. **E2E test automation in CI**
5. **Visual regression testing**
6. **Performance monitoring in CI**
7. **Automatic stale PR/issue management**

---

**Last Updated**: October 16, 2025  
**Automation Version**: 1.0  
**Maintained By**: Development Team
