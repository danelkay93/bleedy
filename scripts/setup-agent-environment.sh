#!/bin/bash
# Agent Environment Setup Script
# Configures environment for optimal multi-agent collaboration
# Supports: Claude Code, GitHub Copilot, CodeRabbit, ChatGPT Codex

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_status() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_header "Multi-Agent Environment Setup"

# Check current directory
if [ ! -f "package.json" ]; then
    print_error "Not in project root directory. Please run from repository root."
    exit 1
fi

print_status "Current directory: $(pwd)"

# 1. Verify required tools
print_header "Verifying Required Tools"

check_tool() {
    if command -v $1 &> /dev/null; then
        VERSION=$($1 --version 2>&1 | head -1)
        print_success "$1 is available: $VERSION"
        return 0
    else
        print_warning "$1 is not available"
        return 1
    fi
}

check_tool "node"
check_tool "npm"
check_tool "git"
check_tool "python3"

# GitHub CLI is critical for multi-agent collaboration
if check_tool "gh"; then
    GH_AVAILABLE=true
else
    GH_AVAILABLE=false
    print_warning "GitHub CLI (gh) not found - some agent features will be limited"
    echo "  Install: https://cli.github.com/"
fi

check_tool "docker" || print_warning "Docker not available - Docker CI workflows will not work locally"
check_tool "curl"
check_tool "jq" || print_warning "jq not available - JSON parsing will be limited"

# 2. Configure Git for PR Access
print_header "Configuring Git for PR Access"

print_status "Adding PR fetch configuration..."
git config --local --get-all remote.origin.fetch | grep -q "refs/pull" || {
    git config --add remote.origin.fetch '+refs/pull/*/head:refs/remotes/origin/pr/*'
    print_success "Added PR head refs to fetch config"
}

git config --local --get-all remote.origin.fetch | grep -q "refs/pull/*/merge" || {
    git config --add remote.origin.fetch '+refs/pull/*/merge:refs/remotes/origin/pr-merge/*'
    print_success "Added PR merge refs to fetch config"
}

# 3. Set up Git aliases for agent collaboration
print_header "Setting Up Git Aliases"

print_status "Creating helpful git aliases..."

git config --local alias.pr-list '!git for-each-ref refs/remotes/origin/pr --format="%(refname:short) %(upstream:track)"' 2>/dev/null || true
print_success "Added alias: git pr-list"

git config --local alias.pr-checkout '!f() { git fetch origin pull/$1/head:pr-$1 && git checkout pr-$1; }; f' 2>/dev/null || true
print_success "Added alias: git pr-checkout <number>"

git config --local alias.pr-diff '!f() { git diff ${2:-master}...origin/pr/$1; }; f' 2>/dev/null || true
print_success "Added alias: git pr-diff <number> [base]"

# 4. Verify npm configuration
print_header "Verifying npm Configuration"

NPM_VERSION=$(npm --version)
print_status "npm version: $NPM_VERSION"

REQUIRED_NPM_VERSION="11.0.0"
if [ "$(printf '%s\n' "$REQUIRED_NPM_VERSION" "$NPM_VERSION" | sort -V | head -n1)" = "$REQUIRED_NPM_VERSION" ]; then
    print_success "npm version is sufficient (>= 11.0.0)"
else
    print_warning "npm version should be >= 11.0.0 for proper patch application"
    print_status "Update with: npm install -g npm@latest"
fi

# 5. Create environment file if it doesn't exist
print_header "Environment Variables"

if [ ! -f ".env.local" ]; then
    print_status "Creating .env.local from template..."
    cat > .env.local << 'EOF'
# Local environment variables for development
# DO NOT commit this file to version control

# Multi-agent collaboration
MULTI_AGENT_MODE=true
AGENT_NAME=

# GitHub configuration (if needed)
# GITHUB_TOKEN=

# Development settings
NODE_ENV=development
VITE_APP_TITLE=Bleedy

# Add your local environment variables below
EOF
    print_success "Created .env.local"
    print_warning "Configure .env.local with your settings"
else
    print_success ".env.local already exists"
fi

# 6. Verify husky setup
print_header "Husky Pre-commit Hooks"

if [ -d ".husky" ]; then
    print_success "Husky directory exists"
else
    print_warning "Husky not initialized"
    print_status "Initialize with: npx husky init"
fi

# 7. Test GitHub CLI if available
if [ "$GH_AVAILABLE" = true ]; then
    print_header "GitHub CLI Configuration"

    if gh auth status &> /dev/null; then
        print_success "GitHub CLI is authenticated"

        # Test PR access
        print_status "Testing PR access..."
        if gh pr list --limit 1 &> /dev/null; then
            print_success "Can access PRs via GitHub CLI"
        else
            print_warning "Cannot access PRs - check repository permissions"
        fi
    else
        print_warning "GitHub CLI not authenticated"
        print_status "Authenticate with: gh auth login"
    fi
fi

# 8. Create agent collaboration shortcuts
print_header "Creating Agent Shortcuts"

# Create a simple script to get PR reviews
if [ "$GH_AVAILABLE" = true ]; then
    cat > /tmp/test-pr-access.sh << 'EOF'
#!/bin/bash
# Quick test of PR access
gh pr list --limit 5 --json number,title,author,state
EOF
    chmod +x /tmp/test-pr-access.sh
    print_success "Test script created: /tmp/test-pr-access.sh"
fi

# 9. Summary and next steps
print_header "Setup Summary"

echo ""
echo "Environment Status:"
echo "  ✓ Project structure verified"
echo "  ✓ Git configured for PR access"
if [ "$GH_AVAILABLE" = true ]; then
    echo "  ✓ GitHub CLI available"
else
    echo "  ! GitHub CLI not available (install recommended)"
fi
echo "  ✓ Git aliases created"
echo "  ✓ Environment template created"
echo ""

print_header "Next Steps for Multi-Agent Collaboration"

echo ""
echo "1. If GitHub CLI is not authenticated:"
echo "   $ gh auth login"
echo ""
echo "2. Fetch PR references:"
echo "   $ git fetch origin"
echo ""
echo "3. List available PRs:"
echo "   $ gh pr list"
echo "   $ git pr-list  (using alias)"
echo ""
echo "4. Access a specific PR:"
echo "   $ python3 scripts/get_pr_reviews.py <pr_number>"
echo "   $ gh pr view <pr_number>"
echo ""
echo "5. Configure your agent-specific settings:"
echo "   - Claude Code: .claude/project-instructions.md"
echo "   - Copilot: .github/copilot-instructions.md"
echo "   - See: .github/AGENT_COLLABORATION.md"
echo ""

print_header "Setup Complete"

echo ""
echo -e "${GREEN}Multi-agent environment is ready!${NC}"
echo ""
echo "Documentation:"
echo "  - Agent collaboration: .github/AGENT_COLLABORATION.md"
echo "  - PR review access: .github/ACCESSING_PR_REVIEWS.md"
echo "  - DevOps guide: DEVCONTAINER_AND_AUTOMATION.md"
echo ""
