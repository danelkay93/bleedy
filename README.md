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

## Multi-Agent Development

This project supports collaboration between multiple AI agents for enhanced development workflows:

- **Claude Code**: Complex refactoring, feature implementation, documentation
- **GitHub Copilot**: Quick fixes, inline suggestions, chat assistance
- **CodeRabbit**: Automated code reviews, security analysis
- **ChatGPT Codex**: GitHub-integrated task automation

For comprehensive agent collaboration guidelines, see [AGENT_COLLABORATION.md](./.github/AGENT_COLLABORATION.md).

### Agent-Specific Documentation

- **Claude Code**: [.claude/project-instructions.md](./.claude/project-instructions.md)
- **GitHub Copilot**: [.github/copilot-instructions.md](./.github/copilot-instructions.md)

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
