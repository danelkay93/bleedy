# CI/CD Pipeline Documentation

This document provides comprehensive guidelines for understanding, maintaining, and troubleshooting the CI/CD pipelines for the Bleedy project.

## Table of Contents

1. [Overview](#overview)
2. [Workflows](#workflows)
3. [Best Practices](#best-practices)
4. [Troubleshooting](#troubleshooting)
5. [Maintenance](#maintenance)

## Overview

The Bleedy project uses GitHub Actions for continuous integration and deployment. Our CI/CD pipeline consists of multiple workflows designed to ensure code quality, security, and reliable deployments.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Actions                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   CI Checks  │  │  Lock File   │  │   Security   │ │
│  │   & Build    │  │     Sync     │  │    Audit     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    Azure     │  │   Staging    │  │  SonarCloud  │ │
│  │  Deployment  │  │   Cleanup    │  │   Analysis   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Workflows

### 1. CI Checks and Build (`ci.yml`)

**Triggers:** Push to master, Pull requests

**Purpose:** Validates code quality and ensures the project builds successfully

**Jobs:**
- **validate-and-build**
  - Installs dependencies with retry mechanism (3 attempts)
  - Runs Prettier format check
  - Executes ESLint
  - Performs TypeScript type checking
  - Builds the project

- **security-audit**
  - Runs `npm audit` to check for vulnerabilities
  - Fails if critical or high severity vulnerabilities found
  - Uploads audit results as artifacts
  - Provides detailed summary in workflow output

**Configuration:**
- Node.js version: 20.x
- Retry attempts: 3 (with 30s delay between attempts)
- Cache: npm dependencies

**Error Handling:**
- Automatic retry for transient npm ci failures
- Cache cleaning on retry to prevent corruption
- Detailed error messages and summaries

### 2. Lock File Synchronization (`lockfile-sync.yml`)

**Triggers:** Pull requests modifying `package.json` or `package-lock.json`, Manual dispatch

**Purpose:** Ensures `package-lock.json` stays in sync with `package.json`

**Process:**
1. Checks if lock file is synchronized
2. Regenerates lock file if out of sync
3. Commits and pushes changes automatically
4. Adds informative PR comment

**Best Practices Enforced:**
- Never manually edit `package-lock.json`
- Always commit lock file changes with `package.json` updates
- Use `npm ci` in CI/CD pipelines

### 3. Azure Static Web Apps Deployment (`azure-static-web-apps-*.yml`)

**Triggers:** Push to master, Pull requests

**Purpose:** Deploys the application to Azure Static Web Apps

**Features:**
- Validates build output before deployment
- Retry mechanism for npm ci
- Enhanced error messages for deployment failures
- Success/failure notifications
- Automatic cleanup of staging environments on PR closure

**Configuration:**
- App location: `/`
- Output location: `dist`
- Node.js version: 20.x

**Error Messages:**
Provides actionable feedback for common failures:
- Staging environment limit reached
- API token issues
- Build output problems
- Network connectivity issues

### 4. Azure Staging Cleanup (`azure-staging-cleanup.yml`)

**Triggers:** Weekly schedule (Sundays at 2 AM UTC), Manual dispatch

**Purpose:** Monitors and manages Azure staging environments

**Features:**
- Lists all open PRs with active staging environments
- Provides visibility into staging environment usage
- Creates alerts when approaching Azure limits (10 staging environments on free tier)
- Supports dry-run mode for testing

**Manual Trigger:**
```bash
# Via GitHub UI: Actions → Azure Staging Cleanup → Run workflow
# Options: dry_run (true/false)
```

### 5. SonarCloud Analysis (`sonarcloud.yml`)

**Triggers:** Push to master, Pull requests

**Purpose:** Performs static code analysis for code quality

**Configuration:**
- Project key: `danelkay93_bleedy`
- Organization: `earthly-serenity`

### 6. Post-Merge Cleanup (`post-merge-cleanup.yml`)

**Triggers:** PR closure (merged only)

**Purpose:** Cleans up consolidated PRs and branches

**Features:**
- Detects consolidation PRs
- Closes related PRs
- Deletes obsolete branches
- Adds cleanup summary

## Best Practices

### Package Management

#### Lock File Management

**DO:**
✅ Always run `npm install` after pulling changes
✅ Commit `package-lock.json` with `package.json` updates
✅ Use `npm ci` in CI/CD pipelines (faster and more reliable)
✅ Let the automated workflow fix sync issues

**DON'T:**
❌ Never manually edit `package-lock.json`
❌ Don't ignore lock file changes in git
❌ Don't use `npm install` in CI/CD pipelines
❌ Don't commit with out-of-sync lock files

#### Dependency Updates

```bash
# Check for outdated dependencies
npm outdated

# Update a specific package
npm update <package-name>

# Update to latest versions (breaking changes possible)
npm update --latest

# Always test after updates
npm run build
npm run test:unit
```

### Security

#### Running Security Audits

```bash
# Run audit locally
npm audit

# Get detailed report
npm audit --json > audit-report.json

# Fix automatically fixable issues
npm audit fix

# Fix with breaking changes (use with caution)
npm audit fix --force
```

#### Vulnerability Management

1. **Critical/High Severity**: Address immediately
   - Review the vulnerability details
   - Update the affected package
   - Test thoroughly before merging
   - Monitor for patches if no fix available

2. **Moderate Severity**: Address in next sprint
   - Evaluate risk vs. effort
   - Plan update in regular cycle
   - Consider workarounds if needed

3. **Low Severity**: Address in maintenance cycle
   - Monitor for severity changes
   - Include in bulk updates
   - Document known issues

### Build Optimization

#### Chunk Size Management

The project uses manual chunk splitting for optimal performance:

```typescript
// vite.config.ts
build: {
  chunkSizeWarningLimit: 1000, // Increased for PyScript dependencies
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

**Guidelines:**
- Keep vendor chunks separate from application code
- Group related libraries together
- Monitor chunk sizes after adding new dependencies
- Adjust `chunkSizeWarningLimit` only when justified

### Azure Deployment

#### Staging Environment Limits

**Free Tier Limits:**
- Maximum 10 staging environments (one per PR)
- Unlimited production deployments

**Best Practices:**
- Close or merge PRs promptly
- Limit concurrent open PRs to 8 or fewer
- Use draft PRs for work-in-progress
- Monitor staging usage with cleanup workflow

#### Deployment Troubleshooting

**"Deployment failed" error:**
1. Check Azure service health
2. Verify API token in repository secrets
3. Review build output validation
4. Check staging environment count
5. Review Azure portal for specific errors

**Manual cleanup if needed:**
```bash
# Via Azure CLI
az staticwebapp environment list --name <app-name>
az staticwebapp environment delete --name <app-name> --environment-name <env-name>
```

## Troubleshooting

### Common Issues

#### 1. npm ci Failures

**Symptoms:**
- "ENOLOCK: no package-lock.json found"
- "Invalid package-lock.json"
- Network timeout errors

**Solutions:**
1. Let retry mechanism complete (automatic)
2. If persistent, regenerate lock file locally:
   ```bash
   rm package-lock.json
   npm install
   git add package-lock.json
   git commit -m "chore: regenerate package-lock.json"
   git push
   ```

#### 2. Build Failures

**Symptoms:**
- TypeScript errors
- Missing dependencies
- Import resolution failures

**Solutions:**
1. Pull latest changes: `git pull`
2. Clean install: `rm -rf node_modules && npm install`
3. Check for patches: Patches are automatically applied during install
4. Verify build locally: `npm run build`

#### 3. Deployment Failures

**Symptoms:**
- Azure deployment timeout
- "Staging limit reached" error
- Build output validation failure

**Solutions:**
1. Check staging environment count (use cleanup workflow)
2. Verify `dist/` directory exists and contains `index.html`
3. Review Azure Static Web Apps logs
4. Manually trigger cleanup workflow if needed

#### 4. Lock File Out of Sync

**Symptoms:**
- "lockfile-sync" workflow creates commits
- npm ci fails with hash mismatch

**Solutions:**
- Automatic: Workflow fixes and commits
- Manual prevention: Always commit lock file with package.json

#### 5. Security Audit Failures

**Symptoms:**
- CI fails on security-audit job
- Critical/high severity vulnerabilities found

**Solutions:**
1. Review vulnerability details in workflow logs
2. Check for available patches: `npm audit fix`
3. Update vulnerable dependencies
4. If no fix available, document and create issue
5. Consider temporary exception if risk is low

### Debug Mode

Enable detailed logging for troubleshooting:

```yaml
# Add to workflow steps
- name: Enable debug logging
  run: |
    echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
    echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV
```

### Viewing Logs

1. Navigate to Actions tab in GitHub
2. Select the workflow run
3. Click on the failed job
4. Expand the failed step
5. Review error messages and context

## Maintenance

### Regular Tasks

#### Weekly
- [ ] Review open PRs and staging environments
- [ ] Check security audit results
- [ ] Monitor workflow success rates

#### Monthly
- [ ] Update dependencies: `npm update`
- [ ] Review and address moderate security vulnerabilities
- [ ] Check for outdated GitHub Actions versions
- [ ] Review and optimize build performance

#### Quarterly
- [ ] Major dependency updates (Vue, Vite, etc.)
- [ ] Review and update workflow configurations
- [ ] Audit and clean up unused workflows
- [ ] Update documentation

### Updating Workflows

When modifying workflows:

1. **Test in a branch first**
   ```bash
   git checkout -b test/workflow-update
   # Make changes
   git push -u origin test/workflow-update
   # Create PR to test workflow
   ```

2. **Use workflow_dispatch for testing**
   ```yaml
   on:
     workflow_dispatch:
     # ... other triggers
   ```

3. **Monitor first runs carefully**
   - Check all jobs complete successfully
   - Verify outputs and artifacts
   - Review error handling paths

4. **Document changes**
   - Update this document
   - Add comments in workflow files
   - Update PR description

### Monitoring

#### Key Metrics to Track

1. **Build Success Rate**: Target > 95%
2. **Average Build Time**: Target < 10 minutes
3. **Deployment Success Rate**: Target > 98%
4. **Security Vulnerabilities**: Target = 0 critical/high

#### Alerts to Configure

- Multiple consecutive build failures
- Security vulnerabilities detected
- Staging environment limit approaching
- Deployment failures

### Emergency Procedures

#### Complete CI Failure

If all builds are failing:

1. Check GitHub Actions status page
2. Verify repository secrets are valid
3. Roll back recent workflow changes
4. Contact GitHub support if platform issue

#### Deployment Outage

If Azure deployments are failing:

1. Check Azure service health
2. Verify production site is still accessible
3. Disable deployment workflow temporarily if needed:
   ```yaml
   jobs:
     build_and_deploy_job:
       if: false  # Temporarily disable
   ```
4. Investigate and fix root cause
5. Re-enable workflow

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [npm Documentation](https://docs.npmjs.com/)
- [Vite Build Documentation](https://vitejs.dev/guide/build.html)
- [SonarCloud Documentation](https://docs.sonarcloud.io/)

## Support

For issues not covered in this documentation:

1. Check existing GitHub Issues
2. Review workflow run logs
3. Create a new issue with:
   - Workflow run link
   - Error messages
   - Steps to reproduce
   - Environment details

---

**Last Updated:** [Current Date]
**Maintainers:** Project Team
**Version:** 1.0.0
