# Claude Code Instructions for Bleedy

## Project Overview

**Bleedy** is a web application for adding bleed margins to images, built with Vue 3, Vite, TypeScript, and PyScript. It allows users to upload images and automatically add professional bleed margins using Python image processing in the browser.

### Key Technologies

- **Frontend**: Vue 3 + TypeScript + Vite
- **UI Framework**: Element Plus with custom wired-elements for sketchy aesthetics
- **Python Integration**: PyScript 2025.5.1 with PIL (Pillow) for image processing
- **Build Tool**: Vite 6.x with hot reload
- **Testing**: Vitest (currently no tests exist)
- **Linting**: ESLint 9.x with Vue/TypeScript support
- **Package Manager**: npm (required version 11.0.0+)

## Build and Development Commands

### Environment Setup

**ALWAYS run `npm install` first** - this project uses patched dependencies and requires proper installation.

```bash
npm install
```

### Development Commands

#### Start Development Server

```bash
npm run dev
```

- Starts Vite dev server on http://localhost:5173/
- Includes hot reload for Vue components
- Takes ~1-2 seconds to start
- PyScript loads asynchronously in browser

#### Build for Production

```bash
npm run build
```

- **Time required**: ~8-10 seconds
- Creates `dist/` directory with production build
- Includes PyScript files and assets
- Warning about chunk sizes is expected (large PyScript dependencies)

#### Type Checking

```bash
npm run type-check
```

- **Known Issues**: Currently fails with 46+ TypeScript errors in components
- Errors relate to:
  - Missing type definitions for never[] arrays
  - Property access on implicit 'any' types
  - Missing Window API types (showOpenFilePicker)
  - RoughJS module declaration issues
- Build still succeeds despite type errors

#### Preview Production Build

```bash
npm run preview
```

- Serves production build locally for testing

### Linting and Formatting

#### ESLint

```bash
npm run lint
```

- **Status**: Working with ESLint 9.x flat config (ES modules format)
- Configuration in `eslint.config.js` uses modern ES modules format
- Automatically ignores `dist/`, `dist-ssr/`, and `node_modules/` folders

#### Prettier

```bash
npm run format
```

- Formats source files in `src/` directory
- Configuration in `.prettierrc.json`
- **Known Issue**: Prettier cache may report formatting issues even when files are correctly formatted
  - Use `npx prettier --check . --cache=false` to verify actual formatting status
  - Use `npx prettier --write . --cache=false` if standard format command seems inconsistent

### Testing

```bash
npm run test:unit
```

- **Status**: No tests currently exist
- Uses Vitest with jsdom environment
- Configuration ready in `vitest.config.ts`

## Project Architecture

### Directory Structure

```
/
├── src/
│   ├── App.vue              # Main application component
│   ├── main.ts              # Vue app entry point
│   ├── components/          # Vue components
│   │   ├── StepManager.vue  # Main workflow component
│   │   ├── ImageProcessor.vue # Image processing UI
│   │   └── steps/           # Step-by-step UI components
│   ├── router/              # Vue Router configuration
│   └── assets/              # Static assets and styles
├── public/
│   ├── pyscript/            # PyScript Python code
│   │   ├── main.py          # Core image processing logic
│   │   └── config.toml      # PyScript configuration
│   └── js/
│       └── bleedy_interop.js # JS-Python bridge
├── patches/                 # npm patches for dependencies
│   ├── roughjs@4.6.6.patch
│   └── wired-elements@3.0.0-rc.6.patch
├── .claude/                 # Claude Code configuration
│   └── project-instructions.md # This file
├── .github/                 # GitHub configuration
│   ├── AGENT_COLLABORATION.md # Multi-agent collaboration guide
│   └── copilot-instructions.md # Copilot configuration
└── dist/                    # Production build output
```

### Key Configuration Files

- `vite.config.ts` - Vite build configuration with Vue, Element Plus, and custom elements
- `tsconfig.*.json` - TypeScript configuration split across multiple files
- `vitest.config.ts` - Test configuration (inherits from Vite config)
- `eslint.config.js` - ESLint configuration (needs ES modules fix)
- `.prettierrc.json` - Code formatting rules

### PyScript Integration

- **Python Version**: Pyodide 0.26.1
- **Python Packages**: Pillow (PIL) for image processing
- **Communication**: Custom event system between Python and Vue
- **Files**:
  - `public/pyscript/main.py` - Image processing algorithms
  - `public/pyscript/config.toml` - PyScript/Pyodide configuration
  - `public/js/bleedy_interop.js` - JavaScript bridge for Python-Vue communication

## Dependencies and Patches

### Critical Dependencies

- `vue@^3.5.13` - Core framework
- `element-plus@^2.9.5` - UI components
- `typescript@~5.7.2` - Type checking
- `vite@^6.0.6` - Build tool

### Patched Dependencies

**IMPORTANT**: This project patches two dependencies. Running `npm install` applies these patches automatically.

1. `roughjs@4.6.6.patch` - Fixes rendering issues
2. `wired-elements@3.0.0-rc.6.patch` - Fixes compatibility with modern browsers

### Known Dependency Issues

- **wired-elements**: Using old RC version (3.0.0-rc.6) that's no longer maintained
- **Browserslist**: Data is 7 months old (warning during build)

## Continuous Integration

### GitHub Workflows

1. **Azure Static Web Apps CI/CD** (`.github/workflows/azure-static-web-apps-thankful-mushroom-08ecc5d1e.yml`)
   - Deploys to Azure on pushes to master
   - Uses standard Node.js build process

2. **CI** (`.github/workflows/ci.yml`)
   - Continuous integration checks on push/PR
   - Runs build and lint checks

3. **SonarCloud** (`.github/workflows/sonarcloud.yml`)
   - Code quality analysis on push/PR

4. **Post-Merge Cleanup** (`.github/workflows/post-merge-cleanup.yml`)
   - Cleanup tasks after merge

5. **Lockfile Sync** (`.github/workflows/lockfile-sync.yml`)
   - Keeps package-lock.json in sync

6. **Azure Staging Cleanup** (`.github/workflows/azure-staging-cleanup.yml`)
   - Cleans up staging environments

## Common Issues and Solutions

### TypeScript Errors

- **Issue**: 46+ type errors across multiple components
- **Impact**: Build succeeds, but `npm run type-check` fails
- **Main Issues**:
  - ImageSelection.vue: Array type inference (`never[]` instead of proper types)
  - Missing Window API types for File System Access API
  - RoughJS module lacks TypeScript declarations
- **Solution**: Add proper type annotations and interface declarations

### ESLint Configuration

- **Status**: Using ESLint 9.x flat config format (ES modules) with proper ignore patterns
- Ignores `dist/`, `dist-ssr/`, and `node_modules/` folders automatically

### PyScript Loading

- **Issue**: PyScript loads asynchronously, may cause timing issues
- **Solution**: Use event listeners for Python-JavaScript communication

### Build Warnings

- Large bundle size warnings are expected due to PyScript/Pyodide dependencies
- Chunk size limit warnings can be ignored for this use case

### Prettier Cache Issues

- **Issue**: `npm run format:check` may report formatting issues due to stale cache
- **Verification**: Use `npx prettier --check . --cache=false` to verify true formatting status
- **Solution**: Run `npx prettier --write . --cache=false` or clear `node_modules/.cache/prettier/`

## Development Guidelines

### Making Changes

1. **Always run `npm install`** after pulling changes (patches may update)
2. **Test in development mode first**: `npm run dev`
3. **Check build**: `npm run build` (ignore type check failures for now)
4. **Verify functionality**: Test image upload and processing in browser

### Component Development

- Vue 3 Composition API with `<script setup>` syntax
- TypeScript for type safety
- Element Plus components for standard UI
- Wired Elements for sketchy aesthetic components

### Python Development

- Edit files in `public/pyscript/`
- Use `console.log()` for debugging (accessible in browser dev tools)
- Follow existing event-driven communication pattern with JavaScript

### Styling

- Uses Element Plus theme
- Custom CSS in `src/assets/`
- Doodle.css and paper-css for hand-drawn aesthetics
- Google Fonts: Cabin Sketch

## Claude Code Specific Features

### Capabilities

Claude Code provides powerful tools for software development:

1. **File Operations**:
   - Read, Write, Edit files with precise control
   - Glob patterns for finding files
   - Grep for searching code content

2. **Code Execution**:
   - Bash commands for running builds, tests, and tools
   - Background process management for long-running tasks

3. **Git Integration**:
   - Create commits with proper messages
   - Push to branches with retry logic
   - Create pull requests via gh CLI

4. **Task Management**:
   - TodoWrite tool for tracking multi-step tasks
   - Proactive task planning and execution

5. **Multi-Agent Collaboration**:
   - Can work alongside Copilot, CodeRabbit, and other agents
   - Follows structured handoff templates
   - Reports progress transparently

### Best Practices for Claude Code

1. **Always use TodoWrite for multi-step tasks** - This helps track progress and ensures nothing is missed
2. **Read files before editing** - Use Read tool to understand context
3. **Test changes locally** - Run `npm run build` and `npm run lint` before committing
4. **Use structured commit messages** - Follow the format in `.github/AGENT_COLLABORATION.md`
5. **Coordinate with other agents** - Check for ongoing work and use handoff templates

### Git Workflow

When making commits:

1. Review changes with `git status` and `git diff`
2. Stage appropriate files
3. Create descriptive commit messages that explain WHY, not just WHAT
4. Always end commits with:
   ```
   Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

When creating PRs:

1. Use `gh pr create` with structured title and body
2. Include summary of changes (not just latest commit)
3. Add test plan with verification steps
4. End with Claude Code attribution

### Limitations

Claude Code operates with certain constraints:

- Cannot access external HTTP/HTTPS URLs directly
- Uses tools for all file and git operations
- Cannot run interactive commands (like `git rebase -i`)
- Works within the repository directory only

### Multi-Agent Collaboration

Claude Code integrates seamlessly with other AI agents in this repository:

**Collaboration Guidelines**:

1. **Check for active work**: Review open issues and PRs before starting
2. **Use handoff templates**: See `.github/AGENT_COLLABORATION.md` for structured communication
3. **Report progress frequently**: Update issues/PRs with status
4. **Coordinate major changes**: Tag other agents when significant architectural changes are planned
5. **Respect branch ownership**: Don't force push to branches owned by other agents

**Working with GitHub Copilot**:
- Copilot has access to GitHub MCP tools for repository operations
- Copilot uses `report_progress` for committing (Claude Code uses git directly)
- Both agents should follow the same code style and commit message conventions

**Working with CodeRabbit**:
- CodeRabbit provides automated code reviews
- Address CodeRabbit's feedback before requesting human review
- Tag with `@coderabbitai review full` for comprehensive review

**Handoff Template** (when passing work to another agent):

```markdown
@[agent-name]

**Context**: [What you've done]

**Current State**:
- Completed: [List]
- In Progress: [List]
- Blocked: [List]

**Next Steps**: [What needs to happen]

**Files Modified**:
- `path/file` - Description

**Testing**: [How to verify]
```

### Documentation Standards

When updating documentation:

1. Keep markdown clean and well-formatted
2. Include code examples with language hints
3. Update "Last Updated" dates
4. Cross-reference related docs
5. Keep technical accuracy paramount

## Multi-Agent Workflows

### Working with Other AI Agents

This repository supports collaboration between multiple AI agents. For comprehensive collaboration guidelines, see `.github/AGENT_COLLABORATION.md`.

### Key Collaboration Points

**Communication Best Practices**:

- Use structured templates for handoffs
- Always include context and file paths in discussions
- Report progress frequently
- Tag relevant agents when needed

**Using Issue and PR Templates**:

- **Agent Tasks**: Use `.github/ISSUE_TEMPLATE/agent_task.md` for AI agent assignments
- **Pull Requests**: Use `.github/PULL_REQUEST_TEMPLATE.md` for all PRs
- Include agent name and task tracking info in PRs

## References

### Documentation

- [AGENT_COLLABORATION.md](../.github/AGENT_COLLABORATION.md) - Comprehensive multi-agent collaboration guide
- [Copilot Instructions](../.github/copilot-instructions.md) - GitHub Copilot configuration
- [CI/CD Guide](../docs/CI_CD_GUIDE.md) - Complete CI/CD documentation
- [CI/CD Quick Reference](../docs/CI_CD_QUICK_REFERENCE.md) - Common CI/CD tasks

### Templates

- [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)
- [Agent Task Template](../.github/ISSUE_TEMPLATE/agent_task.md)
- [Bug Report Template](../.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request Template](../.github/ISSUE_TEMPLATE/feature_request.md)

## Trust These Instructions

These instructions are comprehensive and tested. Only search for additional information if:

1. Commands documented here fail unexpectedly
2. You need to understand implementation details not covered
3. Requirements change beyond current scope

Always prefer the documented commands and configurations over exploration.

---

**Last Updated**: 2025-10-21
**Maintained by**: Claude Code and multi-agent collaboration team
