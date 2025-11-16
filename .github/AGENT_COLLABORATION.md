# Agent Collaboration Guide

## Overview

This guide provides comprehensive information for AI agents (GitHub Copilot Agent, ChatGPT Codex, Gemini Code Assist, Claude Code, Google Jules, CodeRabbit, etc.) working on the Bleedy project. It clarifies technical constraints, communication patterns, and best practices for effective collaboration regardless of the host platform.

## Agent Capability Matrix

| Agent                      | Default Commit Tooling             | Network Access Profile                               | Key Nuances                                                                              |
| -------------------------- | ---------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **GitHub Copilot Agent**   | `report_progress` + PR automation  | GitHub MCP HTTP gateway with GitHub auth             | Prefers `report_progress` checkpoints; surface `gh` helpers when configured.             |
| **ChatGPT Codex**          | `report_progress` (GitHub-managed) | Limited outbound HTTP; GitHub REST available via MCP | Confirm branch context before each commit; Codex dashboards expect concise status notes. |
| **Gemini Code Assist**     | `apply_patch` + Google git proxies | Google-hosted sandbox with curated allow list        | Paste explicit command outputs; document skipped steps that violate policy.              |
| **Claude Code**            | Direct git (`commit`, `push`)      | Anthropic secure proxy with audited HTTP access      | Can use git directly; provide structured diffs and mention safety blocks when triggered. |
| **Google Jules**           | `submit` workflow with auto-commit | Google-aligned HTTP allow list and strict logging    | Provide deterministic QA commands and reproducible steps.                                |
| **CodeRabbit**             | Automated review comments          | GitHub API access for PR/issue operations            | Cannot commit directly; provides automated reviews and suggestions.                      |
| **Other / Unknown Agents** | Varies                             | Assume restricted                                    | Ask which tools are available before running niche commands.                             |

> **Tip:** When instructions conflict, follow the stricter platform rule (for example, if Gemini disallows a network call that Copilot allows, skip it and note the limitation in your response).

## Active Agents

The following AI agents may work on this repository:

- **@copilot** - GitHub Copilot for code changes and PR management
- **@claudecode** - Claude Code for complex refactoring and systematic tasks
- **@codex** - OpenAI Codex for code review and fixes
- **@gemini** - Google Gemini for analysis
- **@coderabbitai** - CodeRabbit for automated code reviews
- **@code-factor** - Code quality analysis
- **@snyk-bot** - Security vulnerability scanning
- **@dependabot** - Dependency updates
- **@jules** - Additional AI assistant

**Agent Selection**: Start with unlimited-usage agents (Copilot, CodeRabbit) for most tasks. Escalate to specialized agents (Claude Code) when their unique capabilities are needed.

## GitHub MCP Server

This repository uses GitHub's official Model Context Protocol (MCP) server for enhanced agent capabilities.

### Configuration

The MCP server is configured in `.mcp/config.json`:
- Provides standardized GitHub operations (PR management, issue creation, etc.)
- Requires `GITHUB_TOKEN` environment variable
- Available to agents that support MCP (check your agent's documentation)

### Using MCP vs. Direct Git

- **Use MCP**: For PR operations, issue management, GitHub API access
- **Use Direct Git**: For local commits, branch operations, file changes
- **Refer to agent-specific docs**: Each agent may have different MCP capabilities

## Technical Limitations

### Network Access

- **Limited outbound HTTP/HTTPS access is available** – agents can usually contact public APIs (including GitHub) when authenticated tooling is configured.
- **Prefer repository-provided tools** – use MCP helpers or curated scripts before resorting to ad-hoc `curl`/`wget` calls.
- **Mind rate limits** – cache responses when practical and avoid unnecessary polling.
- **Workarounds for Reviews**: If HTTP access fails, paste the actual review comments into PR comments, reference specific files and line numbers directly, and quote the exact code or suggestion that needs addressing.

### Git Operations

Agents typically cannot:
- Directly execute `git merge` across branches
- Force push or rebase without appropriate tools
- Access other branches beyond their assigned branch

Agents can:
- Read git history and diffs
- Create changes that are committed via specialized tools
- View branch status and commit logs
- Use MCP tools for GitHub operations (if available)
- Run builds, tests, and linters locally
- Leverage the `npm run qa` helper to execute lint/build/test in one command

## Communication Patterns

### 1. Agent-to-Agent Handoffs

When handing off work to another agent, include:

```markdown
@agent-name

**Context**: [Brief description of what was done]

**Remaining Work**:
- [ ] Task 1
- [ ] Task 2

**Important Notes**:
- Constraint or consideration 1
- Constraint or consideration 2

**Files Modified**:
- path/to/file1.ts (reason)
- path/to/file2.py (reason)

**Testing Status**: [What has been tested, what needs testing]
```

### 2. Requesting Reviews

When requesting a review from another agent:

```markdown
@agent-name

Please review the following changes:

**File**: path/to/file.ts
**Lines**: 10-25
**Change**: [Description]
**Concern**: [What to check]

**Expected**: [What should happen]
**Actual**: [What currently happens, if applicable]
```

### 3. Reporting Completion

When completing a task:

```markdown
**Completed**: [Brief description]

**Commit**: abc1234

**Changes**:
- ✅ Item 1
- ✅ Item 2

**Testing**: [Results of testing]

**Next Steps**: [Optional - what should be done next]
```

## Collaboration Workflows

### Workflow 1: Code Review and Fix

1. **CodeRabbit** identifies issues and leaves review comments
2. **Copilot** or other agent reads the review comments (pasted in PR)
3. Agent makes fixes and commits
4. Agent mentions original reviewer: "@coderabbitai - Fixed in commit abc1234"

### Workflow 2: Feature Development

1. **Primary agent** creates initial implementation
2. **Primary agent** mentions other agent for review
3. User pastes any external review comments into PR
4. **Secondary agent** addresses feedback
5. Final testing and merge

### Workflow 3: Security and Dependencies

1. **Snyk** or **Dependabot** identifies security issues
2. User creates issue or PR comment with details
3. **Copilot** or other agent implements fixes
4. Automated scans validate the fix

## Best Practices

### For All Agents

1. **Always Check Current State First**
   ```bash
   git status
   git log --oneline -10
   npm run build  # or appropriate build command
   ```

2. **Test Before Committing**
   - Run linters: `npm run lint`
   - Run tests: `npm test` (if tests exist)
   - Build: `npm run build`
   - Verify no regressions

3. **Make Minimal Changes**
   - Change only what's necessary
   - Don't refactor unrelated code
   - Don't fix unrelated issues

4. **Document Changes**
   - Update README if needed
   - Update inline comments for complex logic
   - Note breaking changes clearly

5. **Use Structured Commits**
   - Clear, descriptive commit messages
   - Reference issue numbers
   - Group related changes

### For Code Reviews

1. **Be Specific**
   - Quote exact code snippets
   - Provide line numbers
   - Suggest specific alternatives

2. **Provide Context**
   - Explain WHY a change is needed
   - Reference documentation or standards
   - Note potential impacts

3. **Be Actionable**
   - Clear request vs. suggestion
   - Priority (must-fix vs. nice-to-have)
   - Acceptance criteria

## Common Issues and Solutions

### Issue: Agent Can't Access Review URL

**Problem**: Agent asked to review https://github.com/user/repo/pull/123#review-456

**Solution**:
```markdown
Instead of the URL, paste the review content:

**File**: src/components/Example.vue
**Line**: 45
**Comment**: "This function should handle null values"
**Suggestion**:
\`\`\`typescript
if (value === null) return defaultValue;
\`\`\`
```

### Issue: Conflicting Agent Changes

**Problem**: Two agents made changes to the same file

**Solution**:
1. User decides which changes to keep
2. User manually merges if needed
3. User pastes the final desired state in a comment
4. One agent implements the resolution

### Issue: Test Failures After Changes

**Problem**: CI/CD fails after agent commits

**Solution**:
1. Agent checks local test results first
2. If tests pass locally but fail in CI, investigate environment differences
3. Document any known failures in PR description
4. Don't commit if tests fail locally

## Task Templates

### Template: Bug Fix

```markdown
**Bug**: [Description]
**File**: path/to/file
**Line**: [Line number if known]
**Expected**: [What should happen]
**Actual**: [What currently happens]
**Fix**: [Proposed solution]

**Testing**:
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regressions
```

### Template: Feature Addition

```markdown
**Feature**: [Description]
**Files Affected**:
- path/to/file1 (new)
- path/to/file2 (modified)

**Implementation**:
- [ ] Core functionality
- [ ] Error handling
- [ ] Documentation
- [ ] Tests (if applicable)

**Testing**:
- [ ] Feature works as expected
- [ ] Edge cases handled
- [ ] No breaking changes
```

### Template: Refactoring

```markdown
**Refactoring**: [Description]
**Reason**: [Why this change]
**Scope**: [What's included]

**Changes**:
- [ ] Extract function/component
- [ ] Rename for clarity
- [ ] Simplify logic

**Testing**:
- [ ] All tests pass
- [ ] Functionality unchanged
- [ ] Performance impact: [none/positive/negative]
```

## Agent-Specific Documentation

Each agent has its own configuration and instruction files:

- **Claude Code**: `.claude/README.md` - References main docs, Claude Code specifics
- **GitHub Copilot**: `.github/copilot-instructions.md` - Copilot-specific configuration
- **All Agents**: This file - Universal collaboration guide

When starting work:

1. Read your agent-specific documentation first
2. Refer to this collaboration guide for multi-agent workflows
3. Follow the templates and patterns documented here
4. Update documentation when discovering new patterns

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
4. Commit changes using your agent's standard method
5. Verify committed files are appropriate

### Pull Request Standards

- Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
- Keep changes focused and minimal
- Update documentation if needed
- Ensure all CI checks pass

## Escalation

If an agent encounters issues beyond its capabilities:

1. **Document the blocker** clearly in a PR comment
2. **Tag the user** to request intervention
3. **Suggest alternatives** if possible
4. **Preserve work done** so it's not lost

Example:
```markdown
@danelkay93

I've encountered a limitation that prevents me from completing this task:

**Issue**: [Description]
**Attempted**: [What I tried]
**Blocker**: [Specific limitation]

**Options**:
1. [Alternative approach]
2. [Manual intervention needed]
3. [Different agent might help]

**Work Completed**:
- ✅ Part A (commit abc1234)
- ⏸️ Part B (blocked)
```

## Updates to This Document

This document should be updated when:
- New agents are added to the project
- Workflow patterns change
- Common issues are identified
- Technical limitations change

Last Updated: 2025-11-15
