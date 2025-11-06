# bleedy

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

### Unified Quality Checks for Agents

```sh
npm run qa
```

- Runs ESLint, builds the project, and executes the Vitest suite in one command
- Accepts additional options (for example `npm run qa -- --with-typecheck`) to include slower checks when needed
- Designed to simplify common validation workflows for multi-agent collaboration

## Consolidation & Automation Playbook

- Review the [Consolidated Task Guide](./CONSOLIDATED_TASK_GUIDE.md) for a single-source summary of the seven-PR merge, automation setup, review resolution steps, and post-merge expectations.
- Pair it with the quick commands in [docs/AGENT_TOOLKIT.md](./docs/AGENT_TOOLKIT.md) when coordinating across multiple agents.
- Consult [`.github/AGENT_COLLABORATION.md`](./.github/AGENT_COLLABORATION.md) for cross-platform agent guidance covering GitHub Copilot Agent, ChatGPT Codex, Gemini Code Assist, Claude Code, and Google Jules workflows.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. For detailed information about our CI/CD pipelines, including:

- Workflow descriptions and configurations
- Best practices for package management and security
- Troubleshooting common issues
- Maintenance procedures

Please see the [CI/CD Guide](./docs/CI_CD_GUIDE.md).

### Quick Reference

- **Lock file sync**: Automatically maintained by GitHub Actions
- **Security audits**: Run on every PR and push to master
- **Build optimization**: Uses manual chunking for optimal performance
- **Azure deployment**: Automatic with staging environment management

For more details, consult the comprehensive [CI/CD documentation](./docs/CI_CD_GUIDE.md).

