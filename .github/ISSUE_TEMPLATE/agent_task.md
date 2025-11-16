---
name: Agent Task
about: Create a task for an AI agent (GitHub Copilot, ChatGPT Codex, etc.)
title: '[AGENT] '
labels: 'agent-task'
assignees: ''
---

## Task Description

<!-- Provide a clear, concise description of what needs to be done -->

## Context

<!-- Provide background information and context for this task -->

**Related Issues/PRs**:

- #

**Dependencies**:

- [ ] Task/Issue #
- [ ] PR #

## Requirements

<!-- List specific requirements and acceptance criteria -->

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Technical Details

**Affected Components**:

- Component 1
- Component 2

**Files to Modify** (if known):

- `path/to/file1`
- `path/to/file2`

**Technical Approach** (if applicable):

<!-- Describe the preferred or suggested technical approach -->

## Testing Requirements

<!-- Describe how the changes should be tested -->

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing steps:
  1. Step 1
  2. Step 2
  3. Step 3

## Documentation Updates

<!-- List any documentation that needs to be updated -->

- [ ] README.md
- [ ] API documentation
- [ ] Code comments
- [ ] Other:

## Success Criteria

<!-- What does "done" look like for this task? -->

- [ ] All requirements implemented
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] PR merged

## Additional Context

<!-- Add any other context, screenshots, or examples -->

## Agent Assignment

**Preferred Agent**: @[agent-name] <!-- e.g., @copilot, @claude, @codex -->

**Estimated Complexity**: <!-- Low / Medium / High / Unknown -->

**Priority**: <!-- Low / Medium / High / Critical -->

**Task Type Recommendations** (consider usage limits and costs):
- Quick fixes → GitHub Copilot (unlimited, use first)
- Simple features → GitHub Copilot (unlimited, use first)
- Code review → CodeRabbit (automated, unlimited)
- Documentation → GitHub Copilot first, Claude Code if complex
- Multi-file refactoring → Claude Code (when Copilot can't handle)
- Complex debugging → Claude Code (when Copilot can't solve)
- Feature implementation → Copilot first, escalate to Claude Code if needed

**General Strategy:** Start with Copilot (unlimited), escalate to Claude Code (limited/costly) only when needed.

See `.github/AGENT_COLLABORATION.md` for detailed agent capabilities and trade-offs.

---

**For the assigned agent**: Please acknowledge this task and outline your implementation plan before starting work. Use the templates in `.github/AGENT_COLLABORATION.md` for status updates.

**For Claude Code**: Use TodoWrite to track progress and keep this issue updated with your task list.
