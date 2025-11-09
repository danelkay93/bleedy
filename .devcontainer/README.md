# Development Container Configuration

This directory contains the development container (devcontainer) configuration for the Bleedy project, optimized for multi-agent collaboration.

## Overview

The devcontainer provides a **consistent, reproducible development environment** for all developers and AI agents working on the project, including:

- **Claude Code** - Advanced code generation and refactoring
- **GitHub Copilot** - Inline code suggestions
- **CodeRabbit** - Automated code reviews
- **ChatGPT Codex** - GitHub-integrated automation
- **Human developers** - Traditional development

## What's Included

### Base Image

- **Node.js 20** (Debian Bookworm)
- Matches production environment and `@tsconfig/node20` configuration

### Pre-installed Tools

1. **GitHub CLI (`gh`)** - Essential for PR access and GitHub operations
2. **Docker-in-Docker** - For running Docker-based CI locally
3. **Git** (latest) - With enhanced configuration
4. **Python 3** - For automation scripts
5. **Build tools** - gcc, make, etc.
6. **Utilities** - jq, curl, wget, vim, nano

### VS Code Extensions

Automatically installed when opening in VS Code:

- **Vue.volar** - Vue 3 support
- **ESLint** - Linting
- **Prettier** - Code formatting
- **Python** - Python development
- **GitHub Copilot** - AI pair programming
- **GitLens** - Enhanced git integration
- **Docker** - Container management
- **GitHub Pull Requests** - PR management

### Configuration Features

1. **Automatic setup** - Runs `postCreateCommand.sh` after container creation
2. **Port forwarding** - Vite dev (5173) and preview (4173) servers
3. **Volume mounts** - Persistent npm cache and bash history
4. **Git PR refs** - Configured to fetch PR references
5. **Environment variables** - Multi-agent mode enabled

## Quick Start

### Using VS Code

1. Install the **Dev Containers** extension
2. Open the project in VS Code
3. Click "Reopen in Container" when prompted
4. Wait for setup to complete (~2-5 minutes first time)

### Using Command Line

```bash
# Build and start the container
docker build -t bleedy-devcontainer -f .devcontainer/Dockerfile .

# Run the container
docker run -it -v $(pwd):/workspace -p 5173:5173 -p 4173:4173 bleedy-devcontainer

# Inside container, run setup
cd /workspace
bash .devcontainer/postCreateCommand.sh
```

## Post-Creation Setup

The `postCreateCommand.sh` script automatically:

1. ✅ Installs npm dependencies
2. ✅ Configures git for PR refs
3. ✅ Sets up git aliases
4. ✅ Makes scripts executable
5. ✅ Runs agent environment setup
6. ✅ Verifies build
7. ✅ Displays quick start guide

## Environment Variables

Copy `.env.example` to `.env.local` and configure:

```bash
cp .env.example .env.local
# Edit .env.local with your settings
```

Key variables:

- `MULTI_AGENT_MODE=true` - Enables multi-agent features
- `GITHUB_TOKEN` - For API access (optional)
- `AGENT_NAME` - Identifies which agent is working

## GitHub CLI Setup

After container is created, authenticate GitHub CLI:

```bash
gh auth login
```

This enables:

- PR listing and viewing
- Issue management
- Repository operations
- API access

## Testing the Setup

Verify everything is working:

```bash
# Check tools
node --version    # Should show v20.x
npm --version     # Should show v11.x+
gh --version      # Should show latest
python3 --version # Should show Python 3.x

# Test project
npm run dev       # Start dev server
npm run build     # Build project
npm run lint      # Lint code

# Test multi-agent features
bash scripts/setup-agent-environment.sh
python3 scripts/get_pr_reviews.py --help
```

## Customization

### Adding Tools

Edit `Dockerfile` to add new tools:

```dockerfile
RUN apt-get update && apt-get install -y \
    your-new-tool \
    && apt-get clean
```

### Adding VS Code Extensions

Edit `devcontainer.json`:

```json
"extensions": [
  "publisher.extension-name"
]
```

### Changing Ports

Edit `devcontainer.json`:

```json
"forwardPorts": [5173, 4173, 8080]
```

## Troubleshooting

### Container Won't Build

```bash
# Clean rebuild
docker system prune -a
docker build --no-cache -t bleedy-devcontainer -f .devcontainer/Dockerfile .
```

### npm install Fails

```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### GitHub CLI Not Authenticated

```bash
gh auth login
# Follow prompts to authenticate
```

### Git Config Issues

```bash
# Reset git config
git config --local --unset-all remote.origin.fetch
bash scripts/setup-agent-environment.sh
```

## Multi-Agent Collaboration

### For AI Agents

After container setup:

1. **Authenticate GitHub CLI** (if possible in your environment)
2. **Run environment setup**: `bash scripts/setup-agent-environment.sh`
3. **Read collaboration docs**: `.github/AGENT_COLLABORATION.md`
4. **Check PR access guide**: `.github/ACCESSING_PR_REVIEWS.md`

### For Human Developers

1. **Use the devcontainer** for consistent environment
2. **Coordinate with agents** using templates in `.github/`
3. **Review agent changes** via PR templates
4. **Provide feedback** that agents can parse and act on

## Files in This Directory

- `devcontainer.json` - Dev container configuration
- `Dockerfile` - Container image definition
- `postCreateCommand.sh` - Post-creation setup script
- `README.md` - This file

## Related Documentation

- [Multi-Agent Collaboration Guide](../.github/AGENT_COLLABORATION.md)
- [Accessing PR Reviews](../.github/ACCESSING_PR_REVIEWS.md)
- [DevOps Guide](../DEVCONTAINER_AND_AUTOMATION.md)
- [Claude Code Instructions](../.claude/project-instructions.md)
- [Copilot Instructions](../.github/copilot-instructions.md)

## Performance Tips

1. **Use volume mounts** - Keeps npm cache persistent
2. **Rebuild selectively** - Only rebuild when Dockerfile changes
3. **Close unused terminals** - Saves resources
4. **Use multi-stage builds** - If adding complex tools

## Security Notes

1. **Never commit `.env.local`** - Contains sensitive tokens
2. **Use GitHub secrets** - For CI/CD credentials
3. **Rotate tokens regularly** - GitHub tokens should be rotated
4. **Review Dockerfile changes** - Before merging PRs

## Support

For issues with the devcontainer:

1. Check this README and related documentation
2. Search existing GitHub issues
3. Create a new issue with the `devcontainer` label
4. Tag relevant agents for collaboration

---

**Last Updated**: 2025-10-21
**Maintained by**: Multi-agent collaboration team
