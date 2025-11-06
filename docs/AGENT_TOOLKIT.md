# Agent Toolkit Quickstart

This guide collects the most useful commands and workflows for AI and human collaborators working on the Bleedy project. It is formatted for quick consumption by GitHub Copilot Agent, ChatGPT Codex, Gemini Code Assist, Claude Code, Google Jules, and human maintainers.

## Core Validation Commands

| Purpose | Command | Notes |
| --- | --- | --- |
| Install dependencies | `npm install` | Required before running any project script (applies patched deps automatically). |
| Run full QA sweep | `npm run qa` | Executes ESLint, Vite build, and Vitest sequentially with friendly logging. |
| Include TypeScript checks | `npm run qa -- --with-typecheck` | Adds the slower `vue-tsc` pass when TypeScript coverage is required. |
| Skip portions of QA | `npm run qa -- --skip-tests` | Combine with other flags like `--skip-lint` or `--skip-build` for docs-only updates. |
| Check formatting | `npm run format:check` | Uses Prettier; run `npm run format` to auto-fix. |

## Branch and PR Awareness

Staying aware of the repository state prevents duplicated work across agents.

| Task | Command | Tip |
| --- | --- | --- |
| Show current branch | `git branch --show-current` | Include this in handoff notes for clarity. |
| View concise status | `git status -sb` | Captures staged/unstaged file lists quickly. |
| Review recent history | `git log --oneline --decorate --graph -5` | Adjust the `-5` depth as needed. |
| List open PRs (requires GitHub CLI) | `gh pr list --limit 20 --search "repo:danelkay93/bleedy"` | Authenticate once per session. |
| Check CI runs (GitHub CLI) | `gh run list --limit 5 --branch <branch>` | Helps confirm whether QA has already passed. |

## Collaboration Checklist

1. **Read existing documentation**: `.github/AGENT_COLLABORATION.md` details protocols and templates; `CONSOLIDATED_TASK_GUIDE.md` summarizes automation, review handling, and consolidation context.
2. **Plan updates**: confirm task scope, related branches, and outstanding PRs.
3. **Implement changes**: follow the coding standards in `README.md` and component-specific guidelines.
4. **Validate quickly**: use `npm run qa` for the baseline checks.
5. **Share context**: include command outputs (`git status -sb`, QA results) in handoffs or PR descriptions.

## Cross-Agent Defaults

| Agent | Commit Helper | QA Expectation | Notes |
| --- | --- | --- | --- |
| GitHub Copilot Agent | `report_progress` | Capture `npm run qa` (or explain skip) before commit. | Include staged-file summary in commit message prompt. |
| ChatGPT Codex | `report_progress` | Provide concise QA bullet list. | Mention if external URLs were inaccessible. |
| Gemini Code Assist | `apply_patch` / proxy commit | Paste exact command output and flag policy blocks. | Prefer deterministic commands; avoid network calls without confirmation. |
| Claude Code | `commit` / `open_pr` | Include diff-oriented summary in QA notes. | Quote any safety warnings verbatim. |
| Google Jules | `submit` workflow | Provide reproducible QA steps with inputs/flags. | Group related doc updates into one submission. |

## Troubleshooting Tips

- If `npm run qa` fails, rerun individual steps (lint/build/test) to isolate the cause.
- For repeated lint failures, ensure your editor respects the ESLint + Prettier configuration; rerun `npm install` if plugins go missing.
- When network-dependent commands hang, confirm connectivity with a simple `curl https://api.github.com` (subject to rate limits).
- When collaborating asynchronously, paste relevant log excerpts into discussions to maintain shared context.

_Last updated: 2025-10-29_
