# Summary of Changes

This document summarizes all changes made across all files to ensure that functionality hasn't been removed or changed inadvertently.

## Added
- Added `docs/CHANGELOG.md` to document each change with short explanations.
- Added basic sanity tests for Github Copilot Workspace validation in `tests/sanity.test.js`.

## Changed
- Refactored `src/App.vue` for better readability and maintainability.
- Added comments for clarity in `src/App.vue`.
- Refactored `src/components/ImageProcessor.vue` for better readability and maintainability.
- Added comments for clarity in `src/components/ImageProcessor.vue`.
- Improved code structure in `src/components/ImageSelection.vue`.
- Added comments for clarity in `src/components/ImageSelection.vue`.
- Improved code structure in `src/components/StepManager.vue`.
- Added comments for clarity in `src/components/StepManager.vue`.
- Updated dependencies in `package.json` to fix npm vulnerabilities.
- Removed superfluous static imports and fixed dynamic imports in `src/main.ts`.
- Fixed validation loop issue in `src/components/ImageProcessingProgress.vue`.
- Ensured proper configuration for deployment and added steps to deploy to Azure static web app in `.github/workflows/azure-static-web-apps-thankful-mushroom-08ecc5d1e.yml`.
- Updated PyScript version to the latest in `index.html` and checked for new additions to improve PyScript integration with Vue.
