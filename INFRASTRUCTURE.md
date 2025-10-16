# Infrastructure and Automation Setup

This document provides an overview of the Infrastructure as Code (IaC) and automation setup for the Bleedy project.

## Overview

The Bleedy project uses modern DevOps practices including:

- **Infrastructure as Code (IaC)** with Pulumi and Python
- **Automation Scripts** using Python and Plumbum
- **GitHub Actions** for CI/CD orchestration
- **Docker** for containerization
- **Monitoring** strategy documentation

## Directory Structure

```
bleedy/
├── infrastructure/          # Pulumi IaC definitions
│   ├── __main__.py         # Main Pulumi program
│   ├── Pulumi.yaml         # Pulumi project config
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Pulumi documentation
├── automation/             # Automation scripts
│   ├── scripts/           
│   │   ├── post_merge_cleanup.py    # Post-merge PR cleanup
│   │   └── branch_manager.py        # Branch management
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Automation documentation
├── .github/workflows/      # GitHub Actions workflows
│   ├── ci.yml             # CI checks and build
│   ├── pulumi.yml         # Infrastructure deployment
│   ├── docker-compose.yml # Container orchestration
│   ├── branch-management.yml  # Automated branch cleanup
│   └── post-merge-cleanup.yml # Post-merge automation
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # Multi-stage Docker build
├── nginx.conf             # Nginx configuration
└── MONITORING.md          # Monitoring strategy
```

## Quick Start

### Prerequisites

1. **Node.js 20.x** - For application development
2. **Python 3.12** - For infrastructure and automation
3. **Docker** - For containerization
4. **Pulumi CLI** - For infrastructure management
5. **GitHub CLI** (optional) - For GitHub operations

### Setup

#### 1. Install Application Dependencies
```bash
npm install
```

#### 2. Install Infrastructure Dependencies
```bash
cd infrastructure
pip install -r requirements.txt
```

#### 3. Install Automation Dependencies
```bash
cd automation
pip install -r requirements.txt
```

#### 4. Configure Pulumi (Optional)
```bash
cd infrastructure
pulumi login
pulumi stack select dev
```

## Components

### 1. Infrastructure as Code (Pulumi)

**Location:** `infrastructure/`

Pulumi manages infrastructure resources using Python. Currently provides a foundation for:
- Azure Static Web Apps configuration
- Future infrastructure resources

**Usage:**
```bash
cd infrastructure
pulumi preview  # Preview changes
pulumi up       # Apply changes
```

**Documentation:** See [infrastructure/README.md](infrastructure/README.md)

### 2. Automation Scripts

**Location:** `automation/scripts/`

Python scripts for automated repository management:

#### post_merge_cleanup.py
Automates cleanup after consolidation PRs are merged.

```bash
python automation/scripts/post_merge_cleanup.py --pr-number 18 --dry-run
```

#### branch_manager.py
Manages branches: list, cleanup, protect, sync.

```bash
# List all branches
python automation/scripts/branch_manager.py list

# Cleanup stale branches
python automation/scripts/branch_manager.py cleanup --older-than 180 --dry-run

# Protect a branch
python automation/scripts/branch_manager.py protect --branch master
```

**Documentation:** See [automation/README.md](automation/README.md)

### 3. GitHub Actions Workflows

**Location:** `.github/workflows/`

#### ci.yml
Continuous Integration workflow:
- Format checking
- Linting
- Type checking
- Building

Runs on: Push to master, pull requests

#### pulumi.yml
Infrastructure deployment workflow:
- Preview on pull requests
- Deploy on master branch
- Manual deployment trigger

Runs on: Infrastructure file changes, manual trigger

#### docker-compose.yml
Container orchestration workflow:
- Build Docker images
- Test services
- Security scanning with Trivy

Runs on: Dockerfile changes, manual trigger

#### branch-management.yml
Automated branch management:
- Weekly stale branch reports
- Manual branch cleanup
- Branch protection

Runs on: Weekly schedule, manual trigger

#### post-merge-cleanup.yml
Post-merge automation:
- Cleanup consolidated PRs
- Delete obsolete branches
- Add summary comments

Runs on: PR merge, manual trigger

### 4. Docker Configuration

**docker-compose.yml:** Multi-service orchestration
- Web service (development)
- Nginx service (production)

**Dockerfile:** Multi-stage build
- Builder stage: Builds the application
- Production stage: Nginx serving
- Development stage: Vite dev server

**nginx.conf:** Production web server configuration

**Usage:**
```bash
# Development
docker-compose up web

# Production
docker-compose --profile production up nginx

# Build and test
docker-compose build
```

### 5. Monitoring Strategy

**Location:** `MONITORING.md`

Comprehensive monitoring documentation covering:
- Infrastructure monitoring
- Application performance monitoring (APM)
- Log management
- Alerting strategy
- Tool recommendations (Datadog, Sentry, etc.)

**Documentation:** See [MONITORING.md](MONITORING.md)

## GitHub Actions Secrets

Required secrets for workflows:

### For Pulumi Workflow
- `PULUMI_ACCESS_TOKEN` - Pulumi Cloud access token

### For Azure Deployment (existing)
- `AZURE_STATIC_WEB_APPS_API_TOKEN_THANKFUL_MUSHROOM_08ECC5D1E` - Azure deployment token

### For Automation Scripts
Scripts use `GITHUB_TOKEN` (automatically provided by GitHub Actions)

## Development Workflow

### 1. Local Development
```bash
npm install
npm run dev
```

### 2. Testing Changes
```bash
npm run build          # Build the application
npm run type-check     # Type checking
npm run lint           # Linting
```

### 3. Container Testing
```bash
docker-compose up --build web
```

### 4. Infrastructure Changes
```bash
cd infrastructure
pulumi preview         # Preview changes
pulumi up             # Apply (requires PULUMI_ACCESS_TOKEN)
```

### 5. Automation Testing
```bash
# Always use --dry-run first
python automation/scripts/branch_manager.py list
python automation/scripts/post_merge_cleanup.py --pr-number 18 --dry-run
```

## CI/CD Pipeline

### On Pull Request
1. CI checks run (format, lint, type-check, build)
2. Docker images are built and tested
3. Pulumi preview shows infrastructure changes
4. Security scans run on Docker images

### On Merge to Master
1. All CI checks pass
2. Application builds and deploys to Azure
3. Infrastructure changes are applied (if any)
4. Post-merge cleanup runs (if consolidation PR)

### Scheduled Tasks
1. Weekly stale branch report
2. Regular security scans

## Best Practices

### Infrastructure
- Always run `pulumi preview` before `pulumi up`
- Use stack-specific configuration
- Keep secrets in Pulumi config with encryption
- Document all infrastructure changes

### Automation Scripts
- Always test with `--dry-run` first
- Use descriptive commit messages
- Handle errors gracefully
- Log all operations

### Docker
- Use multi-stage builds to minimize image size
- Run security scans regularly
- Keep base images updated
- Use specific version tags

### GitHub Actions
- Use caching for dependencies
- Fail fast on critical errors
- Use matrix builds for multiple environments
- Keep workflows DRY (Don't Repeat Yourself)

## Troubleshooting

### Pulumi Issues
```bash
pulumi login          # Re-authenticate
pulumi refresh        # Sync state with actual infrastructure
pulumi cancel         # Cancel pending operations
```

### Python Script Issues
```bash
# Check environment variables
echo $GITHUB_TOKEN
echo $GITHUB_REPOSITORY

# Reinstall dependencies
pip install -r automation/requirements.txt --upgrade
```

### Docker Issues
```bash
# Clean up
docker-compose down -v
docker system prune -f

# Rebuild
docker-compose build --no-cache
```

### GitHub Actions Issues
- Check workflow logs in GitHub Actions tab
- Verify secrets are set correctly
- Ensure branch permissions are correct
- Check workflow syntax with `actionlint`

## Future Enhancements

### Infrastructure
- [ ] Define Azure Static Web Apps in Pulumi code
- [ ] Add custom domain configuration
- [ ] Set up CDN with Azure Front Door
- [ ] Implement infrastructure testing

### Automation
- [ ] Add more automation scripts (e.g., release management)
- [ ] Implement automatic dependency updates
- [ ] Add PR labeling automation
- [ ] Create issue management scripts

### Monitoring
- [ ] Implement error tracking with Sentry
- [ ] Add APM with Datadog or similar
- [ ] Set up log aggregation
- [ ] Create custom dashboards

### CI/CD
- [ ] Add E2E tests
- [ ] Implement progressive deployment
- [ ] Add smoke tests
- [ ] Set up staging environment

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Plumbum Documentation](https://plumbum.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Azure Static Web Apps](https://docs.microsoft.com/en-us/azure/static-web-apps/)

## Contributing

When adding new infrastructure or automation:

1. Document all changes in relevant README files
2. Test thoroughly with dry-run/preview modes
3. Update this document with new components
4. Add examples and usage instructions
5. Consider security implications
6. Review and update monitoring needs

## Support

For issues or questions:
- Check documentation in respective directories
- Review GitHub Actions logs
- Consult tool-specific documentation
- Create an issue in the repository

---

Last updated: 2025-10-16
