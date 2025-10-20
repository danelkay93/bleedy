# Documentation

This directory contains historical documentation for the Bleedy project.

## ⚠️ Important: Documentation Consolidated

**All DevOps, CI/CD, infrastructure, and automation documentation has been consolidated into a single source of truth:**

### 📖 [DEVCONTAINER_AND_AUTOMATION.md](../DEVCONTAINER_AND_AUTOMATION.md)

This comprehensive guide includes:
- **Development Environment**: Setup, verification, and devcontainer info
- **CI/CD Pipeline**: Docker CI, workflows, lock file management
- **Infrastructure as Code**: Pulumi configuration and deployment
- **Automation**: Python-based branch and environment management
- **Workflows Reference**: Complete workflow documentation
- **Troubleshooting**: Solutions to common issues
- **Best Practices**: Package management, git workflow, security

## Legacy Documentation (Archived)

The following files are maintained for historical reference but are superseded by the consolidated guide:

- `CI_CD_GUIDE.md` - Original CI/CD documentation (see [DEVCONTAINER_AND_AUTOMATION.md](../DEVCONTAINER_AND_AUTOMATION.md) sections: CI/CD Pipeline, Workflows Reference, Troubleshooting)
- `CI_CD_QUICK_REFERENCE.md` - Quick reference (see [DEVCONTAINER_AND_AUTOMATION.md](../DEVCONTAINER_AND_AUTOMATION.md) section: Best Practices)
- `IMPLEMENTATION_CHECKLIST.md` - Implementation tracking (see project management tools)

## Quick Links for New Developers

1. Start with the main [README](../README.md)
2. Read [DEVCONTAINER_AND_AUTOMATION.md](../DEVCONTAINER_AND_AUTOMATION.md) - especially:
   - Development Environment section
   - CI/CD Pipeline section
   - Best Practices section
3. Review [.github/copilot-instructions.md](../.github/copilot-instructions.md) for development guidelines

## Additional Resources

- [Main README](../README.md) - Project overview and setup
- [DEVCONTAINER_AND_AUTOMATION.md](../DEVCONTAINER_AND_AUTOMATION.md) - **Primary DevOps documentation**
- [.github/copilot-instructions.md](../.github/copilot-instructions.md) - Development guidelines
- [.github/AGENT_COLLABORATION.md](../.github/AGENT_COLLABORATION.md) - Multi-agent collaboration
- [automation/README.md](../automation/README.md) - Automation scripts
- [infrastructure/README.md](../infrastructure/README.md) - IaC details

## Contributing

When adding documentation:

1. **Be Clear**: Write for someone unfamiliar with the project
2. **Be Concise**: Use bullet points and short paragraphs
3. **Include Examples**: Show, don't just tell
4. **Keep Updated**: Update docs when you change code
5. **Cross-Reference**: Link to related documentation

## Documentation Standards

- Use Markdown format
- Include a table of contents for long documents
- Use code blocks with language hints
- Include examples for complex procedures
- Keep a "Last Updated" date at the bottom
- Version documentation when making significant changes

## Feedback

If you find documentation issues:

1. Create a GitHub issue with the `documentation` label
2. Include:
   - Which document needs improvement
   - What's unclear or missing
   - Suggestions for improvement

---

**Last Updated:** 2025-10-16
