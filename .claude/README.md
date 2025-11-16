# Claude Code Configuration

Claude Code operates as one agent among equals in this repository.

## Quick Start

See main documentation:
- [Agent Collaboration](../.github/AGENT_COLLABORATION.md) - Multi-agent guidelines
- [Development Environment](../DEVCONTAINER_AND_AUTOMATION.md) - DevOps and automation
- [Copilot Instructions](../.github/copilot-instructions.md) - Copilot configuration

## Project Overview

**Bleedy** - Web app for adding bleed margins to images

**Stack**: Vue 3 + TypeScript + Vite + PyScript + Element Plus

**Key Commands**:
```bash
npm install  # Always run first (applies patches)
npm run dev   # Start dev server (localhost:5173)
npm run build # Build for production (~8-10s)
npm run lint  # Run ESLint
```

## Claude Code Specifics

### Tools Available

- **TodoWrite** - Task tracking (use for complex multi-step tasks)
- **Direct git access** - Can commit and push directly
- **Bash** - Full shell access
- **File operations** - Read, Write, Edit tools

### When to Use Claude Code

**Best for**:
- Complex multi-file refactoring requiring systematic planning
- Feature implementation needing task decomposition
- Deep debugging across multiple files
- CI/CD workflow development

**Not ideal for**:
- Simple fixes → Use @copilot (unlimited usage)
- Quick edits → Use @copilot
- Code review → Use @coderabbitai (automated, unlimited)

**Strategy**: Start with unlimited agents (Copilot, CodeRabbit). Escalate to Claude Code when their unique capabilities justify the usage cost.

### Git Workflow

Claude Code can commit and push directly:

```bash
# Changes are committed with descriptive messages
# Includes "Generated with Claude Code" footer
git add .
git commit -m "message"
git push -u origin <branch-name>
```

**Branch naming**: Must start with `claude/` and end with matching session ID (enforced by server)

**Push retries**: Up to 4 retries with exponential backoff for network errors

### Task Management

Use TodoWrite for complex tasks:
- Track multi-step implementations
- Show progress to users
- Ensure no tasks are forgotten

### Repository-Specific Notes

1. **npm version**: Requires npm 11.0.0+ for proper patch application
2. **Patched dependencies**: Always run `npm install` first
3. **ESLint 9.x**: Uses flat config (`eslint.config.js`)
4. **No tests yet**: `npm test` will fail
5. **Build warnings**: Large chunk size warnings are expected (PyScript)

### Testing Before Commit

Always verify:
```bash
npm run lint   # Must pass
npm run build  # Must complete successfully
```

### Multi-Agent Coordination

When handing off to other agents:
- Use templates from `.github/AGENT_COLLABORATION.md`
- Mention agents with @ (e.g., @copilot, @coderabbitai)
- Paste review content (don't use URLs - agents can't access them)
- Reference specific files and line numbers

### GitHub MCP Server

This repo uses GitHub's official MCP server (`.mcp/config.json`):
- Claude Code uses direct git (not MCP for git operations)
- Other agents may use MCP for GitHub API access
- See `.github/AGENT_COLLABORATION.md` for details

### Development Environment

**Devcontainer available**: See `.devcontainer/README.md`
- Node.js 20 base image
- Pre-installed: GitHub CLI, Python 3, Docker-in-Docker
- Auto-setup via `postCreateCommand.sh`

**Environment script**: `bash scripts/setup-agent-environment.sh`
- Configures git for PR refs
- Creates helpful git aliases
- Verifies tool availability

## Additional Resources

- **DEVCONTAINER_AND_AUTOMATION.md** - Full DevOps guide
- **.github/ACCESSING_PR_REVIEWS.md** - How to access PR reviews programmatically
- **OVERHAUL_STRATEGY.md** - Recent modernization strategy
- **docs/** - Architecture, design patterns, Python integration

## Common Tasks

### Feature Implementation
1. Use TodoWrite to create task list
2. Implement systematically
3. Test with `npm run build && npm run lint`
4. Commit with clear message
5. Push to `claude/*` branch

### Bug Fixes
1. Investigate using file search tools
2. Fix and test locally
3. Verify no regressions
4. Commit and push

### Refactoring
1. Plan changes (TodoWrite)
2. Make minimal, focused changes
3. Test thoroughly
4. Document if needed

---

**Last Updated**: 2025-11-15
**For detailed information**: See main documentation files listed above
