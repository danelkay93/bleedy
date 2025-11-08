# Documentation

This directory contains comprehensive documentation for the Bleedy project.

## Available Guides

### [Consolidated Task Guide](../CONSOLIDATED_TASK_GUIDE.md)

Unified summary of the seven-PR consolidation, automation suite, review resolution steps, and post-merge checklist.

**Contents:**

- Consolidation outcomes and validation snapshot
- Automation workflows and local Husky setup
- Review dismissal templates and post-merge checklist

**Target audience:** Maintainers and collaborators continuing the consolidation workstream

### [CI/CD Guide](./CI_CD_GUIDE.md)

Comprehensive guide to understanding, maintaining, and troubleshooting the CI/CD pipelines.

**Contents:**

- Workflow descriptions and configurations
- Best practices for package management
- Security audit procedures
- Troubleshooting common issues
- Maintenance schedules
- Emergency procedures

**Target audience:** All developers, DevOps engineers, maintainers

### [CI/CD Quick Reference](./CI_CD_QUICK_REFERENCE.md)

Quick reference for common CI/CD tasks and commands.

**Contents:**

- Daily operation commands
- Workflow management
- Common troubleshooting steps
- Useful aliases
- Emergency procedures

**Target audience:** Developers working with the project daily

### [Agent Toolkit Quickstart](./AGENT_TOOLKIT.md)

Condensed command and collaboration reference for AI and human contributors, aligned with GitHub Copilot Agent, ChatGPT Codex, Gemini Code Assist, Claude Code, and Google Jules conventions.

**Contents:**

- Frequently used validation commands (including the `npm run qa` helper)
- Branch and PR awareness tips
- Collaboration and troubleshooting checklists

**Target audience:** Multi-agent collaborators and reviewers

## Quick Links

### For New Developers

1. Start with the main [README](../README.md)
2. Review the [CI/CD Guide](./CI_CD_GUIDE.md) - sections: Overview, Workflows, Best Practices
3. Bookmark the [Quick Reference](./CI_CD_QUICK_REFERENCE.md)

### For Debugging CI Issues

1. Check the [Troubleshooting section](./CI_CD_GUIDE.md#troubleshooting) in CI/CD Guide
2. Use the [Quick Reference](./CI_CD_QUICK_REFERENCE.md) for commands

### For Maintenance

1. Follow the [Maintenance section](./CI_CD_GUIDE.md#maintenance) in CI/CD Guide
2. Review workflow files in `.github/workflows/`

## Additional Resources

- [Main README](../README.md) - Project setup and basic commands
- [FUTURE_WORK.md](../FUTURE_WORK.md) - Planned enhancements
- [TODO.md](../TODO.md) - Current tasks and priorities
- [GitHub Actions Workflows](../.github/workflows/) - Actual workflow files

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

**Last Updated:** 2024-10-29
