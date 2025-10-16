# Next Steps - Subsequent Implementation PR

This document outlines the tasks and features that should be implemented in a subsequent PR after this preliminary setup PR is merged. The preliminary PR (#31) focuses on Copilot instructions, ESLint configuration, and code formatting. The subsequent PR should build upon this foundation with more substantial feature work.

## Context

This preliminary PR establishes:
- ✅ Accurate Copilot instructions for the repository
- ✅ Working ESLint configuration with proper ignore patterns
- ✅ Consistent code formatting across the codebase
- ✅ Documented known issues and workarounds
- ✅ Accurate documentation for tooling (Husky, Prettier, TypeScript)

## Subsequent PR Scope

The following items should be addressed in the next major implementation PR after this one is merged:

### 1. TypeScript Type Safety Improvements

**Priority**: High  
**Estimated Effort**: Medium-Large

#### Issues to Address (46+ TypeScript errors)

**a) ImageSelection.vue - Array Type Inference**
- Fix `never[]` type inference issues
- Add proper type annotations for image arrays
- Define interfaces for image data structures

**b) Window API Types - File System Access API**
- Add type declarations for experimental File System Access API
- Define proper types for `showOpenFilePicker` and related methods
- Consider creating a custom type definition file

**c) RoughJS Module Declarations**
- Add TypeScript declarations for RoughJS library
- Either contribute types to DefinitelyTyped or create local declarations
- Ensure SVG rendering components have proper RoughJS types

**d) Other Component Type Issues**
- Review and fix implicit `any` types across components
- Add proper type guards where needed
- Ensure all refs and reactive data are properly typed

### 2. Pre-commit Hooks Configuration

**Priority**: Medium  
**Estimated Effort**: Small

#### Tasks
- Run `npx husky init` to create `.husky/` directory
- Create pre-commit hook script:
  ```bash
  echo "npm run format:check && npm run lint -- --no-fix" > .husky/pre-commit
  chmod +x .husky/pre-commit
  ```
- Create pre-push hook script:
  ```bash
  echo "npm run type-check && npm run build" > .husky/pre-push
  chmod +x .husky/pre-push
  ```
- Remove or update legacy `.huskyrc.json` file
- Test hooks locally before committing
- Update documentation to reflect actual hook setup

### 3. PyScript Version Check Implementation

**Priority**: Low  
**Estimated Effort**: Small

#### Tasks
- Complete implementation in `scripts/check-pyscript-version.sh`
- Add version parsing logic for:
  - `public/pyscript/config.toml`
  - HTML files referencing PyScript
  - Documentation mentioning PyScript version
- Integrate with Husky pre-commit hooks
- Add tests for the version check script
- Document usage and expected behavior

### 4. Security Vulnerability Remediation

**Priority**: High  
**Estimated Effort**: Small-Medium

#### Tasks
- Address 5 moderate npm security vulnerabilities
- Run `npm audit` to review all vulnerabilities
- Attempt `npm audit fix` for automatic fixes
- Manually update packages if needed
- Test application after updates
- Document any vulnerabilities that cannot be fixed (with justification)

### 5. Test Infrastructure Setup

**Priority**: Medium  
**Estimated Effort**: Medium

#### Tasks
- Create initial test files using Vitest
- Add component tests for key components:
  - ImageSelection.vue
  - ImageProcessor.vue
  - StepManager.vue
- Add utility function tests
- Set up test coverage reporting
- Integrate tests into CI workflow
- Document testing approach and conventions

### 6. Prettier Cache Issue Resolution

**Priority**: Low  
**Estimated Effort**: Small

#### Tasks
- Investigate Prettier cache false positives
- Consider adding `.prettierignore` if needed
- Update CI workflow to use `--cache=false` flag
- Document workaround in contributor guide
- Monitor for upstream Prettier fixes

### 7. Documentation Improvements

**Priority**: Low  
**Estimated Effort**: Small

#### Tasks
- Add CONTRIBUTING.md with development workflow
- Create component documentation in Storybook or similar
- Document PyScript bridge communication protocol
- Add architecture decision records (ADRs) for major decisions
- Update README with current project status

## Implementation Strategy

### Phase 1: Foundation (Immediate)
1. TypeScript type safety improvements (most impactful)
2. Security vulnerability fixes (critical)
3. Pre-commit hooks setup (quick win)

### Phase 2: Quality & Testing (Soon After)
4. Test infrastructure setup
5. PyScript version check implementation

### Phase 3: Polish (Later)
6. Prettier cache investigation
7. Documentation enhancements

## Success Criteria

The subsequent PR should:
- ✅ Reduce TypeScript errors from 46+ to <10
- ✅ Have all security vulnerabilities addressed or documented
- ✅ Include at least 20 unit tests with >70% coverage
- ✅ Have working pre-commit hooks that prevent bad commits
- ✅ Build and run successfully with no new warnings
- ✅ Pass all existing linting and formatting checks

## Notes

- This is a living document and can be updated as priorities change
- Some tasks may be split into separate smaller PRs if appropriate
- New issues discovered during implementation should be added here
- Consider creating GitHub issues for each major task for better tracking

## Related Work

This subsequent PR will complement:
- PR #30: Infrastructure as Code and CI/CD improvements
- PR #31: This preliminary setup PR (Copilot instructions)

## Timeline Estimate

- **Phase 1**: 1-2 weeks
- **Phase 2**: 1 week  
- **Phase 3**: 1 week

**Total estimated effort**: 3-4 weeks of development work

---

**Document Version**: 1.0  
**Created**: October 16, 2025  
**Last Updated**: October 16, 2025  
**Status**: Ready for implementation after PR #31 merge
