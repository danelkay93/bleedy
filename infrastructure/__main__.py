"""
Bleedy Infrastructure as Code using Pulumi

This module defines the infrastructure for the Bleedy application,
currently deployed to Azure Static Web Apps.
"""

import pulumi
from pulumi import Config, export

# Get configuration
config = Config()
stack_name = pulumi.get_stack()
project_name = pulumi.get_project()

# Export basic configuration
export("project_name", project_name)
export("stack_name", stack_name)
export("environment", config.get("environment") or stack_name)

# Note: Azure Static Web Apps infrastructure is currently managed through
# the Azure Portal and GitHub Actions workflow. This Pulumi project serves
# as a foundation for future infrastructure management.

# Future infrastructure resources will be added here:
# - Azure Static Web Apps resource definition
# - Custom domain configuration
# - CDN setup
# - Monitoring and logging infrastructure

pulumi.log.info(f"Pulumi project '{project_name}' initialized for stack '{stack_name}'")
