# Agent Collaboration Guide

## Overview

This guide provides comprehensive information for AI agents (GitHub Copilot, Claude Code, ChatGPT Codex, CodeRabbit, etc.) working on the Bleedy project. It clarifies technical constraints, communication patterns, and best practices for effective collaboration.

## Table of Contents

1. [Technical Limitations](#technical-limitations)
2. [Communication Patterns](#communication-patterns)
3. [Workflow Templates](#workflow-templates)
4. [Best Practices](#best-practices)
5. [Common Issues and Solutions](#common-issues-and-solutions)
6. [Task Templates](#task-templates)

## Technical Limitations

### Environment Constraints

All AI agents operate in sandboxed environments with specific limitations:

#### Network Access

- **Cannot access external HTTP/HTTPS URLs** - This includes GitHub.com URLs, even for this repository
- **Workaround**: Paste review comments or specific content directly into PR/issue comments
- **Note**: Some agents may have internal APIs for GitHub operations (use MCP tools when available)

#### Git Operations

- **Cannot push directly using `git push`** - Must use provided tools like `report_progress`
- **Cannot force push** - No `git reset --hard` or `git rebase` with force push
- **Cannot pull branches** - Cannot resolve merge conflicts directly
- **Cannot clone repositories** - Work with provided repository clone

#### File System

- **Limited to repository directory** - Cannot access files outside the cloned repository
- **Cannot access `.github/agents/` directory** - This contains instructions for other agents

### What Agents CAN Do

- ✅ Read and modify files in the repository
- ✅ Run commands via bash/shell tools
- ✅ Use `report_progress` to commit and push changes (Copilot, Codex)
- ✅ Use git commands directly for commit and push (Claude Code)
- ✅ Access GitHub API via MCP tools (if available)
- ✅ Create and modify issues/PRs (via tools, not direct git)
- ✅ Run builds, tests, and linters locally
- ✅ Use specialized tools for task management (TodoWrite in Claude Code)

## Communication Patterns

### Agent-to-Agent Handoff

When handing off work to another agent:

```markdown
@[agent-name]

**Context**: [Brief description of what you've done]

**Current State**:

- ✅ Completed: [List completed tasks]
- ⚠️ In Progress: [Partially completed work]
- ❌ Blocked: [Issues preventing completion]

**Next Steps**:

1. [Specific action needed]
2. [Expected outcome]

**Files Modified**:

- `path/to/file1` - [Description of changes]
- `path/to/file2` - [Description of changes]

**Testing Notes**:

- [How to verify the changes]
- [Known issues or edge cases]

**References**:

- Issue #[number]
- PR #[number]
- Related discussion: [paste relevant comments]
```

### Review Request

When requesting review from another agent:

```markdown
@[agent-name] review

**Changes Summary**: [High-level description]

**Review Focus**:

- [ ] Code quality and best practices
- [ ] Test coverage
- [ ] Documentation completeness
- [ ] Security considerations

**Specific Questions**:

1. [Question about specific implementation]
2. [Concern about approach]

**Testing**: [How changes were validated]
```

### Completion Report

When finishing a task:

```markdown
**Task Complete**: [Task description]

**Summary**:

- ✅ [Achievement 1]
- ✅ [Achievement 2]
- ✅ [Achievement 3]

**Changes Made**:

- `file1.ts` - [Brief description]
- `file2.vue` - [Brief description]

**Testing**:

- ✅ Build passes: `npm run build`
- ✅ Lint passes: `npm run lint`
- ✅ Manual testing: [Description]

**Commit**: [commit SHA]

**Next Steps**: [Optional follow-up work]
```

## Workflow Templates

### Task Assignment Workflow

1. **User assigns task** to agent via `@[agent]` mention
2. **Agent acknowledges** and outlines plan
3. **Agent reports progress** regularly using `report_progress`
4. **Agent requests review** if needed
5. **Agent completes** with summary

### Multi-Agent Collaboration

1. **Primary agent** creates initial implementation
2. **Primary agent** uses handoff template to pass work
3. **Secondary agent** acknowledges and continues
4. **Secondary agent** reports completion
5. **Either agent** can request review from others

### Code Review Workflow

1. **Author** uses review request template
2. **Reviewer** examines changes using available tools
3. **Reviewer** provides feedback in structured format
4. **Author** addresses feedback
5. **Reviewer** approves or requests further changes

## Best Practices

### For All Agents

1. **Always read existing documentation** before starting work
2. **Use provided tools** (don't try to bypass limitations)
3. **Report progress frequently** using `report_progress`
4. **Include context** in all communications
5. **Paste full content** when referencing external links
6. **Test changes locally** before pushing
7. **Keep commits focused** and well-documented

### Context Preservation

When working on tasks:

- Include relevant file paths in discussions
- Quote specific code sections when discussing changes
- Reference line numbers when applicable
- Paste error messages in full
- Share command outputs that provide context

### Handling Limitations

**When you cannot access a GitHub URL:**

- Ask the user to paste the content
- Explain the limitation clearly
- Document the workaround in your response

**When you cannot push changes:**

- Use `report_progress` tool exclusively
- Never suggest manual git push commands
- Explain that commits will be handled automatically

**When you cannot access a file:**

- Check if the file is in `.github/agents/` (off-limits)
- Verify the path is correct
- Ask the user if the file exists

## Common Issues and Solutions

### Issue: "I cannot access the review comments at [GitHub URL]"

**Solution**: This is expected due to sandbox limitations. Ask the user:

```markdown
I cannot access external URLs from my sandboxed environment. Could you please paste the specific review comments here? This will allow me to address them directly.
```

### Issue: "Git push failed"

**Solution**: Never use `git push` directly. Always use `report_progress`:

```markdown
I cannot push changes directly using git commands. I'll use the `report_progress` tool to commit and push these changes.
```

### Issue: "Cannot resolve merge conflicts"

**Solution**: Merge conflicts must be resolved by the user:

```markdown
I cannot resolve merge conflicts directly as I don't have the ability to pull branches from GitHub. Could you please:

1. Pull the latest changes from master
2. Resolve the conflicts locally
3. Push the resolved branch

Then I can continue with the implementation.
```

### Issue: "Cannot find another agent's changes"

**Solution**: Request the specific file contents:

```markdown
I don't have access to changes made by other agents unless they're in the current branch. Could you please share:

1. The specific files that were modified
2. The commit SHA or PR number
3. The content of the changes if available
```

## Task Templates

### Bug Fix Task

```markdown
**Bug**: [Description of the bug]

**Reproduction Steps**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior**: [What should happen]

**Actual Behavior**: [What actually happens]

**Root Cause**: [Analysis of the issue]

**Fix**: [Description of the solution]

**Testing**: [How to verify the fix]

**Files Modified**:

- `path/to/file` - [Description]
```

### Feature Implementation Task

```markdown
**Feature**: [Feature description]

**Requirements**:

- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Implementation Plan**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Technical Approach**: [High-level design]

**Testing Strategy**: [How to validate]

**Documentation Updates**: [Required doc changes]
```

### Refactoring Task

```markdown
**Refactoring**: [What needs to be refactored]

**Motivation**: [Why this refactoring is needed]

**Approach**:

- [Approach detail 1]
- [Approach detail 2]

**Impact Assessment**:

- Breaking changes: [Yes/No, with details]
- Performance impact: [Analysis]
- Test coverage: [Current and target]

**Validation**: [How to verify nothing broke]
```

## Tool-Specific Notes

### Claude Code

- **Configuration**: Uses `.claude/project-instructions.md` for project-specific instructions
- **Capabilities**:
  - Direct file operations (Read, Write, Edit tools)
  - Bash commands with full shell access
  - Git operations (commit, push, PR creation via gh CLI)
  - Task management via TodoWrite tool
  - Web search and fetch capabilities
- **Strengths**:
  - Excellent for multi-step refactoring and implementation tasks
  - Strong planning and task decomposition via TodoWrite
  - Direct git integration with retry logic
  - Comprehensive file editing with exact string matching
- **Limitations**:
  - Cannot access external HTTP/HTTPS URLs directly (uses WebFetch tool)
  - Cannot run interactive commands (like `git rebase -i`)
  - All operations use tools (no direct system access)
- **Best Use Cases**:
  - Feature implementation with multiple files
  - Complex refactoring tasks
  - Documentation updates
  - CI/CD workflow development
  - Bug fixes requiring systematic investigation
- **Attribution**: Commits include "Generated with Claude Code" footer

### GitHub Copilot Agent

- **Configuration**: Uses `.github/copilot-instructions.md` for project-specific instructions
- Has access to GitHub MCP tools for repository operations
- Can read issues, PRs, and comments via API
- Uses `report_progress` for committing changes
- Cannot access external URLs (HTTP/HTTPS)
- **Best Use Cases**:
  - Quick code completions
  - Inline suggestions
  - Chat-based problem solving

### ChatGPT Codex Connector

- Operates through GitHub integration
- Can create commits and interact with GitHub
- Provides task tracking via Codex dashboard
- May have different tool availability

### CodeRabbit

- Provides automated code reviews
- Can be triggered with `@coderabbitai review full`
- Focuses on code quality and best practices
- Can suggest improvements and identify issues
- **Best Use Cases**:
  - Automated PR reviews
  - Security vulnerability detection
  - Code quality assessment

### Other Agents

- May have varying capabilities
- Always check available tools before starting
- Document any unique limitations discovered
- Update this guide with new findings

## Repository-Specific Guidelines

### Before Making Changes

1. Run `npm install` (patches are applied automatically)
2. Verify current state: `npm run build && npm run lint`
3. Review existing code style and patterns
4. Check for related issues or PRs

### After Making Changes

1. Run linter: `npm run lint`
2. Build the project: `npm run build`
3. Test manually if UI changes
4. Use `report_progress` to commit changes
5. Verify committed files are appropriate

### Pull Request Standards

- Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
- Keep changes focused and minimal
- Update documentation if needed
- Ensure all CI checks pass

## Getting Help

If you encounter issues not covered in this guide:

1. **Check existing documentation** in the repository
2. **Ask the user** for clarification or assistance
3. **Document the issue** for future reference
4. **Update this guide** if you find a solution

## Contributing to This Guide

This guide is a living document. If you discover:

- New limitations or capabilities
- Better workarounds for common issues
- Improved communication patterns
- Tool-specific tips

Please update this guide in your PR with a clear explanation of the addition.

## Agent-Specific Documentation

Each agent has its own configuration and instruction files:

- **Claude Code**: `.claude/project-instructions.md` - Comprehensive project guide with Claude Code specific features
- **GitHub Copilot**: `.github/copilot-instructions.md` - Copilot-specific configuration and guidelines
- **All Agents**: This file (`.github/AGENT_COLLABORATION.md`) - Universal collaboration guide

When working on the project, agents should:
1. Read their agent-specific documentation first
2. Refer to this collaboration guide for multi-agent workflows
3. Follow the templates and patterns documented here
4. Update documentation when discovering new patterns or issues

## Choosing the Right Agent for the Task

Different agents excel at different types of tasks:

| Task Type | Recommended Agent | Reason |
|-----------|------------------|---------|
| Multi-file refactoring | Claude Code | Strong file operations, task planning |
| Quick code fixes | GitHub Copilot | Fast inline suggestions |
| Feature implementation | Claude Code | TodoWrite tracking, systematic approach |
| Code review | CodeRabbit | Automated analysis, security focus |
| Documentation updates | Claude Code | Comprehensive file editing |
| CI/CD workflow development | Claude Code | Direct git/bash access |
| Inline completions | GitHub Copilot | Real-time IDE integration |
| Complex debugging | Claude Code | Systematic investigation tools |

---

**Last Updated**: 2025-10-21
**Maintained by**: Claude Code, GitHub Copilot, ChatGPT Codex, and community contributors
