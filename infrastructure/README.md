# Infrastructure as Code

This directory contains Infrastructure as Code (IaC) definitions for the Bleedy project using Pulumi.

## Overview

This directory is prepared for Pulumi-based infrastructure management. The `pulumi.yml` workflow is configured to deploy infrastructure automatically.

## Setup

To initialize Pulumi infrastructure:

```bash
# Install Pulumi CLI
curl -fsSL https://get.pulumi.com | sh

# Login to Pulumi
pulumi login

# Create a new stack
cd infrastructure
pulumi new azure-python  # or azure-typescript

# Configure stack
pulumi config set azure-native:location EastUS
```

## Structure

When infrastructure code is added, organize it as:

```
infrastructure/
├── Pulumi.yaml          # Pulumi project configuration
├── Pulumi.dev.yaml      # Development stack config
├── Pulumi.prod.yaml     # Production stack config
├── __main__.py          # Main infrastructure code (Python)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Deployment

Infrastructure is deployed automatically via GitHub Actions:

- **Preview on PR**: Shows what changes will be made
- **Deploy on merge**: Applies changes to infrastructure

Manual deployment:

```bash
cd infrastructure

# Preview changes
pulumi preview

# Apply changes
pulumi up

# View current state
pulumi stack output
```

## Current Status

This directory is set up for future Infrastructure as Code initiatives. The workflow is in place and ready for when infrastructure code is added.

## Planned Infrastructure

Future infrastructure components to be managed:

- Azure Static Web Apps configuration
- Azure Storage for artifacts
- Azure CDN configuration
- Monitoring and alerting resources
- DNS and domain configuration

## Security

Secrets and credentials:

- Pulumi Access Token: Stored in GitHub Secrets as `PULUMI_ACCESS_TOKEN`
- Azure credentials: Will be configured in Pulumi config
- Sensitive values: Encrypted using Pulumi secrets

## Contributing

When adding infrastructure code:

1. Follow the Pulumi best practices for the chosen language
2. Add comprehensive comments and documentation
3. Test changes in a development stack first
4. Create PR for preview before merging
5. Monitor deployment in GitHub Actions

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Azure Native Provider](https://www.pulumi.com/registry/packages/azure-native/)
- [Pulumi Best Practices](https://www.pulumi.com/docs/using-pulumi/best-practices/)
