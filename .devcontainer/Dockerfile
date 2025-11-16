# Multi-Agent Development Container for Bleedy
# Optimized for collaboration between Claude Code, GitHub Copilot, CodeRabbit, and other AI agents

FROM node:20-bookworm

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    # Essential development tools
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    # Python for automation scripts
    python3 \
    python3-pip \
    python3-venv \
    # Build tools
    build-essential \
    # Additional tools for multi-agent collaboration
    jq \
    vim \
    nano \
    less \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set up npm global directory with correct permissions
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$NPM_CONFIG_PREFIX/bin:$PATH
RUN mkdir -p /usr/local/share/npm-global \
    && chown -R node:node /usr/local/share/npm-global

# Install global npm packages
RUN npm install -g npm@latest \
    && npm install -g \
    prettier@latest \
    eslint@latest \
    typescript@latest \
    @vue/language-server@latest

# Configure git for PR refs (enables programmatic PR access)
RUN git config --system --add fetch.prune true \
    && git config --system --add core.autocrlf input \
    && git config --system --add pull.rebase false

# Install uv for fast Python package management (system-wide)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh -s -- --install-dir /usr/local/bin

# Set up Python environment with uv
RUN uv pip install --system --no-cache-dir \
    pyyaml \
    requests \
    python-dotenv

# Create command history directory
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir -p /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R node:node /commandhistory \
    && echo "$SNIPPET" >> "/home/node/.bashrc"

# Create workspace directory
RUN mkdir -p /workspace \
    && chown -R node:node /workspace

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Set the default user
USER node

# Set working directory
WORKDIR /workspace
