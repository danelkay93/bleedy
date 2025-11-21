# Agent Collaboration Guide

## Overview

This guide provides comprehensive information for AI copilots (GitHub Copilot Agent, ChatGPT Codex, Gemini Code Assist, Claude Code, Google Jules, CodeRabbit, etc.) working on the Bleedy project. It clarifies technical constraints, communication patterns, and best practices for effective collaboration regardless of the host platform.

## Agent Capability Matrix

| Agent                      | Default Commit Tooling             | Network Access Profile                               | Key Nuances                                                                              |
| -------------------------- | ---------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **GitHub Copilot Agent**   | `report_progress` + PR automation  | GitHub MCP HTTP gateway with GitHub auth             | Prefers `report_progress` checkpoints; surface `gh` helpers when configured.             |
| **ChatGPT Codex**          | `report_progress` (GitHub-managed) | Limited outbound HTTP; GitHub REST available via MCP | Confirm branch context before each commit; Codex dashboards expect concise status notes. |
| **Gemini Code Assist**     | `apply_patch` + Google git proxies | Google-hosted sandbox with curated allow list        | Paste explicit command outputs; document skipped steps that violate policy.              |
| **Claude Code**            | `commit` / `open_pr` helpers       | Anthropic secure proxy with audited HTTP access      | Provide structured diffs and mention safety blocks when they trigger.                    |
| **Google Jules**           | `submit` workflow with auto-commit | Google-aligned HTTP allow list and strict logging    | Provide deterministic QA commands and reproducible steps.                                |
| **Other / Unknown Agents** | Varies                             | Assume restricted                                    | Ask which tools are available before running niche commands.                             |

> **Tip:** When instructions conflict, follow the stricter platform rule (for example, if Gemini disallows a network call that Copilot allows, skip it and note the limitation in your response).

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

- **Limited outbound HTTP/HTTPS access is available** – agents can usually contact public APIs (including GitHub) when authenticated tooling is configured.
- **Prefer repository-provided tools** – use MCP helpers or curated scripts before resorting to ad-hoc `curl`/`wget` calls.
- **Mind rate limits** – cache responses when practical and avoid unnecessary polling.

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
- ✅ Use `report_progress` to commit and push changes
- ✅ Access GitHub API via MCP tools or authenticated CLI clients when available
- ✅ Create and modify issues/PRs (via tools, not direct git)
- ✅ Run builds, tests, and linters locally
- ✅ Leverage the `npm run qa` helper to execute lint/build/test in one command

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

**Solution**: Some environments restrict outbound HTTP/HTTPS access. If you receive a denial, ask the user:

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

### GitHub Copilot Agent

- Uses GitHub MCP to expose `report_progress`, git history lookups, and limited GitHub REST calls.
- Prefers incremental commits—summarize staged changes before invoking `report_progress`.
- Can run authenticated `gh` commands when configured; announce if the CLI is unavailable.

### ChatGPT Codex

- Operates through GitHub's Codex integration with opinionated status dashboards.
- `report_progress` is available, but Codex expects concise summaries (≤5 bullet points) per commit.
- Outbound HTTP is constrained to GitHub domains—ask users to paste external artifacts.

### Gemini Code Assist

- Relies on `apply_patch` and Google-managed git proxies instead of direct `git commit`.
- Command execution is audited; paste exact outputs (trimmed for relevance) in your response body.
- Flag skipped commands explicitly when policy prevents execution.

### Claude Code

- Provides `commit` and `open_pr` helpers that require a final diff summary.
- Anthropic's proxy logs all outbound HTTP—note when a call may trigger safety review.
- If a safety filter blocks an action, include the filter message verbatim and propose a compliant alternative.

### Google Jules

- Automates commits through a `submit` workflow; group related changes into one submission unless the user asks otherwise.
- Emphasizes deterministic QA: list the exact commands you ran and any you intentionally skipped.
- Jules integrates with Google issue trackers—reference issue IDs when available.

### CodeRabbit (Review Agent)

- Provides automated code reviews and can be triggered with `@coderabbitai review full` in PR threads.
- Focuses on code quality, performance, and best practices—respond inline to each thread it opens.

### Other Agents

- Capabilities vary; confirm available tools with `help`/`tools` commands before starting.
- Document unique limitations discovered during a session for future contributors.
- Update this guide via PR when you discover durable differences.

## Repository-Specific Guidelines

### Before Making Changes

1. Run `npm install` (patches are applied automatically)
2. Confirm branch context with `git status -sb` and `git branch --show-current`
3. Review recent activity via `git log --oneline --decorate --graph -5`
4. Check for related issues or PRs using available tooling (for example `gh pr list --limit 20` when authenticated)
5. Review existing code style and patterns

### After Making Changes

1. Run the unified QA helper: `npm run qa`
   - Add `--with-typecheck` when TypeScript validation is required
   - Use `--skip-tests` or related flags for documentation-only updates
2. Test manually if UI changes
3. Use `report_progress` to commit changes
4. Verify committed files are appropriate
5. Capture branch status in handoff notes (`git status -sb`)

### Repository Awareness Checklist

| Task                                | Command                                                   |
| ----------------------------------- | --------------------------------------------------------- |
| Show current branch                 | `git branch --show-current`                               |
| Inspect local branches              | `git branch --sort=-committerdate`                        |
| View remote tracking info           | `git remote -v`                                           |
| Summarize recent history            | `git log --oneline --decorate --graph -10`                |
| List open PRs (requires GitHub CLI) | `gh pr list --limit 20 --search "repo:danelkay93/bleedy"` |
| Check CI status for branch          | `gh run list --limit 5 --branch <branch>`                 |

### Pull Request Standards

- Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
- Keep changes focused and minimal
- Update documentation if needed
- Ensure all CI checks pass

## Getting Help

If you encounter issues not covered in this guide:

1. **Check existing documentation** in the repository
   - Start with the [Agent Toolkit Quickstart](../docs/AGENT_TOOLKIT.md) for command references
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

---

**Last Updated**: 2024-10-29
**Maintained by**: GitHub Copilot Agent, ChatGPT Codex, Gemini Code Assist, Claude Code, Google Jules, and community contributors
