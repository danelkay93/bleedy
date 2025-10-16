# CI/CD Pipeline Maintenance Guide

This document provides guidelines and best practices for maintaining the Bleedy CI/CD pipeline.

## Table of Contents

- [Overview](#overview)
- [Workflows](#workflows)
- [Lock File Management](#lock-file-management)
- [Build Optimization](#build-optimization)
- [Staging Environment Management](#staging-environment-management)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

The Bleedy project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

1. **CI Checks** - Validates code quality, formatting, types, and builds
2. **Azure Static Web Apps Deployment** - Deploys to production and creates PR previews
3. **Staging Cleanup** - Removes unused staging environments
4. **Post-Merge Cleanup** - Cleans up consolidated PRs and branches

## Workflows

### CI Checks (`ci.yml`)

Runs on every push to master and on pull requests. Performs:

- Lock file validation
- Dependency installation
- Code formatting checks
- Linting
- Type checking
- Production build

**Location**: `.github/workflows/ci.yml`

### Azure Static Web Apps Deployment (`azure-static-web-apps-*.yml`)

Handles deployment to Azure Static Web Apps:

- **On Push to Master**: Deploys to production
- **On PR Open/Update**: Creates staging environment with preview URL
- **On PR Close**: Removes staging environment

**Features**:

- Lock file validation before build
- Retry logic for npm ci (up to 3 attempts)
- Deployment summary in GitHub Actions
- Node.js caching for faster builds

**Location**: `.github/workflows/azure-static-web-apps-thankful-mushroom-08ecc5d1e.yml`

### Staging Environment Cleanup (`cleanup-staging.yml`)

Automated cleanup of unused staging environments:

- **Schedule**: Runs weekly on Sundays at 2 AM UTC
- **Manual Trigger**: Can be run manually with dry-run mode
- **Logic**: Removes staging environments for closed PRs

**Configuration Required**:

- `AZURE_CREDENTIALS` secret (service principal)
- `AZURE_RESOURCE_GROUP` secret (optional, defaults to 'bleedy-rg')

**Location**: `.github/workflows/cleanup-staging.yml`

### Post-Merge Cleanup (`post-merge-cleanup.yml`)

Cleans up consolidated PRs and their branches after merge.

**Location**: `.github/workflows/post-merge-cleanup.yml`

## Lock File Management

### Why Lock File Validation Matters

The `package-lock.json` file ensures deterministic dependency installation. When it's out of sync with `package.json`, `npm ci` fails, breaking the build pipeline.

### Validation Script

A validation script runs before every build:

**Location**: `scripts/validate-lockfile.sh`

**What it checks**:

- Lock file exists
- Lock file is in sync with package.json
- npm ci can run successfully

### Common Issues and Fixes

#### Issue: Lock file out of sync

**Symptoms**:

```
npm ci fails with "package-lock.json" error
Validation script reports "Lock file is NOT in sync"
```

**Fix**:

```bash
# Remove the lock file
rm package-lock.json

# Regenerate it
npm install

# Commit the new lock file
git add package-lock.json
git commit -m "chore: regenerate package-lock.json"
```

#### Issue: Different npm versions

**Symptoms**:

```
Lock file format changes between developers
Frequent lock file conflicts
```

**Fix**:

- Ensure all developers use npm 11.0.0+ (specified in package.json)
- Use `corepack enable` to enforce package manager version
- Never manually edit `package-lock.json`

### Best Practices

1. **Never manually edit package-lock.json** - Always use npm commands
2. **Use `npm install`** to add/update dependencies (updates lock file)
3. **Use `npm ci`** in CI environments (enforces lock file)
4. **Commit lock file changes** with dependency updates
5. **Use consistent npm versions** across the team

## Build Optimization

### Chunk Splitting Configuration

The build is optimized using Vite's `manualChunks` feature:

```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'element-plus': ['element-plus', '@element-plus/icons-vue'],
        'vue-vendor': ['vue', 'vue-router', 'pinia'],
        'utilities': ['file-saver', 'jszip']
      }
    }
  },
  chunkSizeWarningLimit: 1500
}
```

**Benefits**:

- Better caching (vendor code changes less frequently)
- Faster initial loads
- Improved parallel loading
- Smaller individual chunks

**Chunks**:

- `element-plus.js` (~880KB) - UI framework
- `vue-vendor.js` (~190KB) - Vue core and state management
- `utilities.js` (~100KB) - File handling utilities
- `index.js` (~150KB) - Application code

### Dynamic vs Static Imports

**Use static imports** for components used in the template:

```typescript
// ✅ Correct
import MyComponent from './MyComponent.vue'

export default {
  components: {MyComponent}
}
```

**Avoid dynamic imports** when component is used in template:

```typescript
// ❌ Incorrect - causes build warnings
export default {
  components: {
    MyComponent: () => import('./MyComponent.vue')
  }
}
```

### Monitoring Build Performance

Watch for these warnings during build:

1. **Dynamic/static import conflicts** - Indicates incorrect import usage
2. **Large chunk warnings** - May need additional chunk splitting
3. **Slow transformation** - Consider optimizing dependencies

## Staging Environment Management

### Automatic Cleanup

The staging cleanup workflow runs weekly and:

1. Lists all staging environments in Azure
2. Checks which PRs are still open
3. Removes staging environments for closed PRs
4. Keeps production and active PR environments

### Manual Cleanup

To manually trigger cleanup:

1. Go to Actions → "Cleanup Staging Environments"
2. Click "Run workflow"
3. Select dry run mode to preview (optional)
4. Click "Run workflow"

### Dry Run Mode

Test the cleanup without deleting anything:

```yaml
dry_run: 'true'
```

This shows what would be deleted in the workflow summary.

### Required Secrets

Set these in repository settings:

```
AZURE_CREDENTIALS        # Service principal JSON
AZURE_RESOURCE_GROUP     # Resource group name (optional)
```

To create service principal:

```bash
az ad sp create-for-rbac \
  --name "bleedy-staging-cleanup" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

## Troubleshooting

### npm ci Failures

**Symptoms**: Build fails at dependency installation

**Check**:

1. Is lock file in sync? Run `scripts/validate-lockfile.sh`
2. Are there network issues? Check npm registry status
3. Is cache corrupted? Retry the workflow

**The workflow includes**:

- Automatic retry (up to 3 attempts)
- 5-second delay between retries
- Detailed error messages

### Azure Deployment Failures

**Symptoms**: Build succeeds but deployment fails

**Common causes**:

1. Invalid Azure token
2. Too many staging environments (cleanup needed)
3. Build output location mismatch

**Solutions**:

1. Verify `AZURE_STATIC_WEB_APPS_API_TOKEN` secret
2. Run staging cleanup workflow
3. Ensure `output_location: 'dist'` matches build output

### Build Performance Issues

**Symptoms**: Slow builds, timeouts

**Solutions**:

1. Check if dependencies need updates
2. Review chunk splitting configuration
3. Consider increasing workflow timeout
4. Use Node.js caching (already enabled)

### Lock File Conflicts

**Symptoms**: Merge conflicts in package-lock.json

**Resolution**:

```bash
# Accept either version
git checkout --theirs package-lock.json
# OR
git checkout --ours package-lock.json

# Then regenerate
npm install

# Commit the result
git add package-lock.json
git commit -m "chore: resolve lock file conflict"
```

## Best Practices

### Dependency Management

1. **Update dependencies regularly** - Use Dependabot
2. **Test updates locally first** - Don't merge untested updates
3. **Keep npm version consistent** - Use packageManager field
4. **Review security alerts** - Address vulnerabilities promptly
5. **Avoid manual package.json edits** - Use npm commands

### Workflow Maintenance

1. **Keep actions up to date** - Update action versions regularly
2. **Monitor workflow runs** - Check for degraded performance
3. **Review staging environments** - Ensure cleanup is working
4. **Test manual workflows** - Verify they work as expected
5. **Document changes** - Update this guide when making changes

### Build Optimization

1. **Monitor chunk sizes** - Keep under warning limit (1500KB)
2. **Profile build times** - Identify slow steps
3. **Use caching effectively** - Node modules, build outputs
4. **Minimize dependencies** - Only add what's necessary
5. **Review build output** - Check for unexpected files

### Security

1. **Rotate secrets regularly** - Azure tokens, service principals
2. **Use least privilege** - Grant minimal required permissions
3. **Review workflow permissions** - Limit GitHub token scope
4. **Audit dependencies** - Run `npm audit` regularly
5. **Keep dependencies updated** - Patch security vulnerabilities

### Code Quality

1. **Run checks locally** - Before pushing to CI
2. **Fix linting errors** - Don't disable rules without reason
3. **Address type errors** - Maintain type safety
4. **Format code consistently** - Use Prettier
5. **Write meaningful commits** - Help reviewers understand changes

## Maintenance Checklist

### Weekly

- [ ] Review failed workflow runs
- [ ] Check staging environment count
- [ ] Review dependency security alerts

### Monthly

- [ ] Update GitHub Actions versions
- [ ] Review and update dependencies
- [ ] Check Azure resource usage
- [ ] Review build performance metrics

### Quarterly

- [ ] Audit Azure permissions
- [ ] Rotate service principal secrets
- [ ] Review and update documentation
- [ ] Evaluate new CI/CD features

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Static Web Apps Docs](https://learn.microsoft.com/en-us/azure/static-web-apps/)
- [Vite Build Optimization](https://vitejs.dev/guide/build.html)
- [npm ci Documentation](https://docs.npmjs.com/cli/v10/commands/npm-ci)
- [Lock File Specification](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json)

## Getting Help

If you encounter issues not covered in this guide:

1. Check workflow logs in GitHub Actions
2. Review recent changes that might have caused the issue
3. Search existing GitHub issues
4. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Relevant logs and error messages
   - What you've tried to fix it
