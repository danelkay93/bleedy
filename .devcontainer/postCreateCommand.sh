#!/bin/bash
# Post-create command for devcontainer
# Runs after container is created to set up the development environment

set -e

echo "🚀 Setting up Bleedy development environment for multi-agent collaboration..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Install npm dependencies
print_status "Installing npm dependencies..."
npm install
print_success "npm dependencies installed"

# Configure git for PR access
print_status "Configuring git for PR refs..."
git config --add remote.origin.fetch '+refs/pull/*/head:refs/remotes/origin/pr/*' || true
git config --add remote.origin.fetch '+refs/pull/*/merge:refs/remotes/origin/pr-merge/*' || true
print_success "Git configured for PR access"

# Try to fetch PR refs (may fail if not authenticated, which is OK)
print_status "Attempting to fetch PR refs..."
git fetch origin 2>/dev/null || print_warning "Could not fetch PR refs (authentication may be needed)"

# Set up git user if not configured
if [ -z "$(git config user.name)" ]; then
    print_warning "Git user.name not set. Set it with: git config user.name 'Your Name'"
fi

if [ -z "$(git config user.email)" ]; then
    print_warning "Git user.email not set. Set it with: git config user.email 'your.email@example.com'"
fi

# Verify GitHub CLI
if command -v gh &> /dev/null; then
    print_success "GitHub CLI (gh) is available"
    # Check auth status (won't fail if not authenticated)
    gh auth status 2>/dev/null && print_success "GitHub CLI is authenticated" || print_warning "GitHub CLI not authenticated. Run: gh auth login"
else
    print_warning "GitHub CLI (gh) is not available"
fi

# Verify Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "Python is available: $PYTHON_VERSION"
else
    print_warning "Python is not available"
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x scripts/*.py 2>/dev/null || true
chmod +x automation/*.py 2>/dev/null || true
print_success "Scripts are executable"

# Run agent environment setup
if [ -f "scripts/setup-agent-environment.sh" ]; then
    print_status "Running agent environment setup..."
    bash scripts/setup-agent-environment.sh
else
    print_warning "Agent environment setup script not found"
fi

# Verify build
print_status "Verifying build..."
if npm run build > /dev/null 2>&1; then
    print_success "Build verification passed"
else
    print_warning "Build verification failed - you may need to run 'npm run build' manually"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Development environment ready!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Quick start commands:"
echo "  npm run dev          - Start development server"
echo "  npm run build        - Build for production"
echo "  npm run lint         - Run ESLint"
echo "  npm run format       - Format code with Prettier"
echo ""
echo "Multi-agent collaboration:"
echo "  See: .github/AGENT_COLLABORATION.md"
echo "  See: .github/ACCESSING_PR_REVIEWS.md"
echo ""
echo "For GitHub operations:"
echo "  gh auth login        - Authenticate with GitHub"
echo "  gh pr list           - List pull requests"
echo "  gh pr view <number>  - View PR details"
echo ""
