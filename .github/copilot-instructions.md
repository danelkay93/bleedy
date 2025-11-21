# Copilot Instructions for Bleedy

> Multi-agent context: For cross-platform conventions covering ChatGPT Codex, Gemini Code Assist, Claude Code, and Google Jules, see [`.github/AGENT_COLLABORATION.md`](./AGENT_COLLABORATION.md) and the [Agent Toolkit Quickstart](../docs/AGENT_TOOLKIT.md).

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

#### Unified QA Helper

```bash
npm run qa
```

- Executes ESLint, Vite build, and Vitest in sequence with helpful logging
- Pass `--with-typecheck` to include the slower Vue TypeScript checks when they are required
- Additional flags like `--skip-tests` are available for documentation-only updates

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

### Pre-commit Hooks (Planned)

- `scripts/check-pyscript-version.sh` - Validates PyScript version consistency
- Currently not integrated with Husky

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

## Agent Collaboration

### Working with Other AI Agents

This repository supports collaboration between multiple AI agents (GitHub Copilot, ChatGPT Codex, CodeRabbit, etc.). For comprehensive collaboration guidelines, see `.github/AGENT_COLLABORATION.md`.

### Key Collaboration Points

**Technical Considerations**:

- Outbound HTTP/HTTPS access is typically available but subject to rate limits and tool configuration
- Cannot push directly using `git push` - must use `report_progress` tool
- Cannot resolve merge conflicts - user must handle these
- Cannot access files in `.github/agents/` directory

**Communication Best Practices**:

- Use structured templates for handoffs (see AGENT_COLLABORATION.md)
- Always include context and file paths in discussions
- Paste full content of review comments when referencing them
- Report progress frequently using `report_progress`

**Handoff Template** (Brief Version):

```markdown
@[agent-name]

**Context**: [What you've done]
**Current State**: [Completed/In Progress/Blocked items]
**Next Steps**: [What needs to happen]
**Files Modified**: [List with descriptions]
**Testing**: [Verification steps]
```

### Using Issue and PR Templates

This repository provides structured templates for better collaboration:

- **Agent Tasks**: Use `.github/ISSUE_TEMPLATE/agent_task.md` for AI agent assignments
- **Bug Reports**: Use `.github/ISSUE_TEMPLATE/bug_report.md` for bugs
- **Feature Requests**: Use `.github/ISSUE_TEMPLATE/feature_request.md` for features
- **Pull Requests**: Use `.github/PULL_REQUEST_TEMPLATE.md` for all PRs

### Multi-Agent Workflows

When multiple agents work on the same task:

1. **Primary agent** creates initial implementation
2. **Primary agent** uses handoff template to transfer work
3. **Secondary agent** acknowledges and continues
4. **Either agent** can request reviews from others
5. **Final agent** completes with comprehensive summary

See `.github/AGENT_COLLABORATION.md` for detailed workflow templates and examples.

## Trust These Instructions

These instructions are comprehensive and tested. Only search for additional information if:

1. Commands documented here fail unexpectedly
2. You need to understand implementation details not covered
3. Requirements change beyond current scope

Always prefer the documented commands and configurations over exploration.
