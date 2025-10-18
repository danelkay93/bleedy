# Bleedy Infrastructure as Code

This directory contains Infrastructure as Code (IaC) definitions for the Bleedy application using [Pulumi](https://www.pulumi.com/) with Python.

## Overview

Bleedy is currently deployed to Azure Static Web Apps. This Pulumi project provides a foundation for managing the infrastructure programmatically and can be extended to include:

- Azure Static Web Apps resource definition
- Custom domain configuration
- CDN setup
- Monitoring and logging infrastructure
- Database resources (if needed)
- API backend resources (if needed)

## Prerequisites

1. **Install Pulumi CLI:**

   ```bash
   curl -fsSL https://get.pulumi.com | sh
   ```

2. **Install Python Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Pulumi Backend:**

   You can use either:
   - Pulumi Cloud (default): Sign up at [app.pulumi.com](https://app.pulumi.com)
   - Self-managed backend: File system, Azure Blob, AWS S3, etc.

   ```bash
   # Login to Pulumi Cloud
   pulumi login

   # Or use local backend
   pulumi login --local
   ```

4. **Configure Azure Credentials** (when managing Azure resources):
   ```bash
   az login
   ```

## Getting Started

### Initialize the Stack

The project includes a `dev` stack by default. To create a new stack:

```bash
cd infrastructure
pulumi stack init production
```

### Configure the Stack

Set required configuration values:

```bash
pulumi config set azure-native:location WestUS2
pulumi config set bleedy-infrastructure:environment production
```

### Preview Changes

Preview infrastructure changes before applying:

```bash
pulumi preview
```

### Deploy Infrastructure

Apply the infrastructure changes:

```bash
pulumi up
```

### View Outputs

View exported values from the stack:

```bash
pulumi stack output
```

## Project Structure

```
infrastructure/
├── __main__.py          # Main Pulumi program
├── Pulumi.yaml          # Project configuration
├── Pulumi.dev.yaml      # Development stack configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Configuration

### Stack Configuration

Each stack can have its own configuration in `Pulumi.<stack-name>.yaml`:

```yaml
config:
  bleedy-infrastructure:environment: production
  azure-native:location: WestUS2
  pulumi:tags:
    value:
      environment: production
      managed-by: pulumi
```

### Secrets Management

Pulumi automatically encrypts sensitive configuration values:

```bash
# Set a secret value
pulumi config set --secret apiKey mySecretValue

# View configuration (secrets are encrypted)
pulumi config
```

## GitHub Actions Integration

### Pulumi Workflow

A GitHub Actions workflow is provided for automated infrastructure deployment:

```yaml
name: Pulumi Infrastructure

on:
  push:
    branches:
      - master
    paths:
      - 'infrastructure/**'

jobs:
  pulumi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd infrastructure
          pip install -r requirements.txt

      - name: Pulumi up
        uses: pulumi/actions@v5
        with:
          command: up
          # Use 'dev' stack for PRs, 'production' for pushes to master
          stack-name: ${{ github.event_name == 'pull_request' && 'dev' || 'production' }}
          work-dir: infrastructure
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```

### Required Secrets

Add these secrets to your GitHub repository:

- `PULUMI_ACCESS_TOKEN`: Your Pulumi access token (from app.pulumi.com)
- `AZURE_CREDENTIALS`: Azure service principal credentials (if using Azure)

## Extending Infrastructure

### Adding Azure Static Web Apps

Example code to add Azure Static Web App resource:

```python
import pulumi_azure_native as azure

# Create resource group
resource_group = azure.resources.ResourceGroup(
    "bleedy-rg",
    location="WestUS2"
)

# Create Static Web App
static_web_app = azure.web.StaticSite(
    "bleedy-app",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=azure.web.SkuDescriptionArgs(
        name="Free",
        tier="Free",
    ),
    branch="master",
    repository_url="https://github.com/danelkay93/bleedy",
    build_properties=azure.web.StaticSiteBuildPropertiesArgs(
        app_location="/",
        api_location="",
        output_location="dist",
    )
)

# Export the default hostname
pulumi.export("endpoint", static_web_app.default_hostname)
```

### Adding Custom Domain

```python
# Add custom domain
custom_domain = azure.web.StaticSiteCustomDomain(
    "bleedy-custom-domain",
    domain_name="bleedy.example.com",
    name=static_web_app.name,
    resource_group_name=resource_group.name
)
```

## Stack Management

### List Available Stacks

```bash
pulumi stack ls
```

### Switch Stacks

```bash
pulumi stack select dev
pulumi stack select production
```

### Delete a Stack

```bash
pulumi stack rm dev
```

### Export/Import Stack State

```bash
# Export stack state
pulumi stack export --file stack-backup.json

# Import stack state
pulumi stack import --file stack-backup.json
```

## Best Practices

1. **Use Stack-Specific Configuration**: Keep environment-specific settings in `Pulumi.<stack>.yaml`
2. **Tag All Resources**: Use tags for cost tracking and resource management
3. **Use Secrets for Sensitive Data**: Always use `pulumi config set --secret` for passwords, tokens, etc.
4. **Review Before Applying**: Always run `pulumi preview` before `pulumi up`
5. **Automate with CI/CD**: Use GitHub Actions for consistent deployments
6. **Version Control**: Keep all Pulumi code in version control
7. **Document Changes**: Update this README when adding new infrastructure components

## Troubleshooting

### "no credentials" Error

Ensure you're logged into Pulumi:

```bash
pulumi login
```

### Azure Authentication Issues

Re-authenticate with Azure:

```bash
az login
az account set --subscription "your-subscription-id"
```

### State Conflicts

If you encounter state conflicts:

```bash
pulumi cancel  # Cancel any pending operations
pulumi refresh # Sync state with actual infrastructure
```

### Stack Locked

If a stack is locked from a previous operation:

```bash
pulumi stack export | pulumi stack import --force
```

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Pulumi Python SDK](https://www.pulumi.com/docs/languages-sdks/python/)
- [Azure Native Provider](https://www.pulumi.com/registry/packages/azure-native/)
- [Pulumi Examples](https://github.com/pulumi/examples)
- [Pulumi Best Practices](https://www.pulumi.com/docs/using-pulumi/best-practices/)

## Future Enhancements

- [ ] Define Azure Static Web Apps resource in code
- [ ] Add custom domain configuration
- [ ] Set up CDN with Azure Front Door
- [ ] Configure monitoring with Azure Application Insights
- [ ] Add cost optimization tags and policies
- [ ] Set up multiple environments (dev, staging, production)
- [ ] Implement infrastructure testing with Pulumi policy packs
