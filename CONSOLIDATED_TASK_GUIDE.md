# Bleedy Consolidated Task Guide

This playbook merges the most useful guidance from the automation setup, automation summary, PR readiness report, and review resolution notes that supported PR #18 (the seven-PR consolidation). Use it as the single source of truth when maintaining the consolidated branch, resolving reviews, or onboarding additional collaborators.

---

## Snapshot

- ✅ All seven outstanding PRs were merged into a single, modernized codebase.
- ✅ Automation now covers post-merge cleanup, dependency hygiene, and unified QA helpers.
- ✅ Documentation, accessibility fixes, and TypeScript safety improvements are in place.
- ⚠️ Husky hooks and the PyScript version guard still need one-time setup per developer.
- ⚠️ 5 moderate npm vulnerabilities remain for follow-up hardening.

---

## Key Outcomes from the Consolidation

| Area                            | Highlights                                                                                                                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Merged PRs**                  | #1 `refactor-cleanup`, #7 `phase1-refactor-pyscript-deps`, #8 `fix/eslint-errors` (base), #10 reverse-conflict resolution, #12 `snyk-upgrade-element-plus-2.9.1`, #14 `snyk-upgrade-element-plus-2.9.5`, #15 `snyk-upgrade-element-plus-2.10.5`. |
| **Dependency Health**           | `element-plus` 2.11.4, `vue` 3.5.22, `vue-router` 4.5.1, PyScript 2025.5.1/Pyodide 0.26.1.                                                                                                                                                       |
| **Type Safety**                 | SVG typing and null guards in `Logo.vue`, missing imports and emit typing fixes in `App.vue` and `ImageSelection.vue`, ref typing cleanup in `ImageGallery.vue`.                                                                                 |
| **Accessibility**               | Replaced global `outline: none` with WCAG-compliant `:focus-visible` styles, improving keyboard navigation.                                                                                                                                      |
| **Configuration Modernization** | ESLint 9 flat config, comprehensive `.github/workflows/ci.yml`, documented `npm run qa` helper, refreshed Copilot instructions.                                                                                                                  |
| **Documentation**               | `CONSOLIDATION_CHANGES.md`, `CODERABBIT_FIXES.md`, `FUTURE_WORK.md`, this guide, and the `docs/` handbook series capture historical context and future plans.                                                                                    |

---

## Automation Suite Overview

### 1. Post-Merge Cleanup (`.github/workflows/post-merge-cleanup.yml`)

- **Trigger**: Runs automatically whenever a PR merges into `master`/`main`.
- **Actions**: Detects consolidation PR metadata, closes PRs #1/#7/#8/#10/#12/#14/#15 with explanatory comments, deletes their branches (`refactor-cleanup`, `phase1-refactor-pyscript-deps`, `fix/eslint-errors`, and the Snyk branches), and posts a final summary.
- **Benefit**: Keeps the repo free of stale PRs/branches without manual intervention.

### 2. CI Quality Gate (`.github/workflows/ci.yml`)

- Runs on pushes and pull requests.
- Executes formatting check (`npm run format:check`), ESLint, TypeScript type check, and production build.
- Intended to be the definitive gate once local Husky hooks are enabled.

### 3. Dependency Hygiene (`.github/dependabot.yml`)

- **npm** updates every Monday at 09:00 UTC (max 5 open PRs).
- **GitHub Actions** updates monthly (max 3 open PRs).
- Automatically applies `dependencies` + `automated` labels, rebases as needed, and ignores major updates for Vue, Element Plus, and Vite unless manually lifted.

### 4. Local Unified QA (`npm run qa`)

- Orchestrates ESLint → Vite build → Vitest with clear section headers.
- Flags: `--with-typecheck` adds `vue-tsc`; `--skip-tests`, `--skip-lint`, and `--skip-build` support documentation-only updates.
- Use this before invoking the heavier CI pipeline.

---

## Developer Setup & Local Automation

> Each contributor needs to perform these one-time steps after cloning.

1. **Install dependencies (applies npm patches automatically):**
   ```bash
   npm install
   ```
2. **Initialize Husky v9 and enable the intended checks:**
   ```bash
   npx husky init
   echo "npm run format:check && npm run lint -- --no-fix" > .husky/pre-commit
   chmod +x .husky/pre-commit
   echo "npm run type-check && npm run build" > .husky/pre-push
   chmod +x .husky/pre-push
   ```
3. **Retire the legacy `.huskyrc.json`** once the `.husky/` directory is active (it targets the old Husky 4 flow).
4. **Wire in the PyScript version guard** after the hook scripts exist:
   ```bash
   echo "bash scripts/check-pyscript-version.sh" >> .husky/pre-commit
   chmod +x scripts/check-pyscript-version.sh
   ```

   - The script still needs its version-parsing logic finalized (tracked in `TODO.md`).
5. **Confirm tooling works locally:**
   ```bash
   npm run qa
   ```

---

## Validation Snapshot (from consolidation QA)

| Check                | Result                                                   | Notes                                                                                   |
| -------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Build                | ✅ `npm run build` (≈11.4s, 1566 modules)                | Expected chunk-size warnings due to PyScript payloads.                                  |
| TypeScript           | ⚠️ Critical issues fixed; ~26 non-blocking errors remain | Missing third-party types, File System Access API declarations, and legacy `any` usage. |
| Linting & Formatting | ✅ ESLint 9 flat config + Prettier alignment             | Occasional Prettier cache hiccups; rerun with `--cache=false` if needed.                |
| Dependency Audit     | ⚠️ 5 moderate dev dependency vulnerabilities             | Documented for follow-up hardening; no production impact.                               |
| Functionality        | ✅ Core Vue workflow + PyScript bridge verified          | Accessibility fixes applied; icons renamed to PascalCase components.                    |

---

## Review Resolution Playbook

The three outstanding reviews on PR #18 were addressed in commits `5999327`, `4f8ba7a`, and `b682a60`. If manual dismissal is still required:

1. **Navigate to [PR #18](https://github.com/danelkay93/bleedy/pull/18).**
2. **For CodeRabbit review:** resolve each conversation or dismiss with the rationale that type safety, accessibility, and null-guard fixes landed in commit `5999327` (see `CODERABBIT_FIXES.md`).
3. **For the package-version review:** confirm upgrades to Vue/Element Plus/Vue Router in commit `4f8ba7a` and reference `CONSOLIDATION_CHANGES.md`.
4. **For the general follow-up review:** cite the documentation sweep (`CONSOLIDATION_CHANGES.md`, this guide) and automation improvements (`b682a60`).
5. **If you lack dismiss permissions**, tag the reviewers with a status comment summarizing the above bullet points and request approval.

Template snippet:

```markdown
All issues raised in this review have been addressed:

- ✅ Type safety + accessibility fixes (commit 5999327; see CODERABBIT_FIXES.md)
- ✅ Dependency versions verified (commit 4f8ba7a; see CONSOLIDATION_CHANGES.md)
- ✅ Documentation & automation updates (commit b682a60; see CONSOLIDATED_TASK_GUIDE.md)
  Please re-review and approve when convenient.
```

---

## Post-Merge Checklist

1. **Verify automation ran:** ensure the post-merge cleanup workflow closed the legacy PRs/branches.
2. **Manual spot checks (if automation was paused):**
   - Close PRs #1/#7/#8/#10/#12/#14/#15.
   - Delete `refactor-cleanup`, `phase1-refactor-pyscript-deps`, `fix/eslint-errors`, and the Snyk branches.
3. **Deployment confidence:** run `npm run build` or `npm run preview` and smoke-test the PyScript flow.
4. **Security maintenance:** plan a follow-up PR to address the remaining npm advisories (see `TODO.md`).
5. **Document future work:** track TypeScript typing backlog, PyScript guard completion, and Husky hook verification in `FUTURE_WORK.md` / `TODO.md`.

---

## Reference Index

- [`CONSOLIDATION_CHANGES.md`](./CONSOLIDATION_CHANGES.md) – Detailed version changes, removed/renamed assets, validation logs.
- [`CODERABBIT_FIXES.md`](./CODERABBIT_FIXES.md) – TypeScript and accessibility fixes from commit `5999327`.
- [`FUTURE_WORK.md`](./FUTURE_WORK.md) & [`TODO.md`](./TODO.md) – Roadmap and actionable tasks.
- [`docs/AGENT_TOOLKIT.md`](./docs/AGENT_TOOLKIT.md) – Quick command reference for multi-agent collaboration.
- [`.github/AGENT_COLLABORATION.md`](./.github/AGENT_COLLABORATION.md) – Platform-aligned playbook for Copilot, Codex, Gemini, Claude, and Jules agents.
- [`README.md`](./README.md) & [`docs/README.md`](./docs/README.md) – Project overview and documentation index.

### Legacy Document Map

For backward compatibility, the historical checklists now redirect here:

| Legacy File                                        | Status                                                                        |
| -------------------------------------------------- | ----------------------------------------------------------------------------- |
| [`AUTOMATION_SETUP.md`](./AUTOMATION_SETUP.md)     | Redirect notice pointing to this guide for local automation setup.            |
| [`AUTOMATION_SUMMARY.md`](./AUTOMATION_SUMMARY.md) | Redirect notice summarizing the automation coverage now tracked here.         |
| [`PR_READINESS.md`](./PR_READINESS.md)             | Redirect notice pointing to this guide for pre-PR validation and review prep. |
| [`REVIEW_RESOLUTION.md`](./REVIEW_RESOLUTION.md)   | Redirect notice directing reviewers to the resolution playbook in this guide. |

_Last updated: 2024-10-29_
