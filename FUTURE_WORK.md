# Future Work & Roadmap for Bleedy.py

This document outlines planned enhancements, refactoring tasks, and feature ideas for the Bleedy.py application. It consolidates items from previous analysis, `TODO.md`, and user requests.

## Phase 1 Completion Notes
Phase 1 focused on initial stabilization:
- PyScript modernized to `2025.5.1`, Pyodide pinned to `0.26.1`.
- PyScript loading splashscreen added.
- Placeholder for PyScript version check hook created.
- JS-PyScript communication refactored (event-based, no DOM polling for results).
- Basic code cleanup (default bleed, removed dead components/deps).
- Initial plan for sketchy UI library overhaul documented in `TODO.md`.
- CI pipeline now runs lint, format check, type check, and build.
- Local ESLint config updated to flat config, Prettier config corrected.

## I. Core Infrastructure & Stability

### 1. Sketchy UI Libraries Overhaul (High Priority)
   - **Objective:** Stabilize or replace the aging sketchy UI libraries to ensure long-term maintainability and remove current patching needs.
   - **Tasks (details in `TODO.md`):**
     - **Fork `wired-elements`:** Create an internal, maintained fork (`bleedy-wired-elements`).
       - Apply existing patch: `patches/wired-elements@3.0.0-rc.6.patch`.
       - Audit and refactor components to use `Rough.js 4.6.6+` API correctly.
       - Goal: Eliminate the need for `patches/roughjs@4.6.6.patch`.
       - Review and update Lit/LitElement dependencies if outdated.
     - **Address `DoodleCSS` and `paper-css`:**
       - Manually verify current maintenance status.
       - If unmaintained/problematic: Absorb styles into project, find alternatives, or replicate effects.
     - **Ultimate Goal:** Remove all files from `patches/` and the `npm.patchedDependencies` section in `package.json`.

### 2. PyScript Enhancements
   - **Full Pre-commit Hook:** Implement and test `scripts/check-pyscript-version.sh` with Husky for robust PyScript version management.
   - **Zipping in Python:** Research and potentially implement image zipping using Python within PyScript (`zipfile` module) if it offers significant advantages over client-side JS `jszip` (e.g., performance, bundle size reduction).

### 3. Comprehensive Testing Strategy (Very High Priority)
   - **Objective:** Achieve robust test coverage to ensure code quality and prevent regressions.
   - **Tasks:**
     - **Unit Testing (Vitest):**
       - Write comprehensive unit tests for all Vue components (props, events, slots, logic).
       - Test all composables (`useImageDownload`, any new ones).
       - Test utility functions and configurations.
       - Configure and enforce code coverage reporting in CI.
     - **Integration Testing (Vitest):** Test interactions between key components (e.g., `ImageProcessor` and its steps, JS-PyScript interop mocks).
     - **E2E Testing (Playwright or Cypress - select one):**
       - Set up the chosen framework.
       - Create E2E tests for all critical user flows.
     - **Python Code Testing:**
       - Research and implement best practices for testing PyScript's Python code (e.g., `add_bleed` function). This might involve extracting logic or using Pyodide's testing utilities if available.
     - **Visual Regression Testing:** Implement tools (e.g., Percy, Applitools, or Playwright-based) to catch unintended UI changes, especially important for the sketchy aesthetic.
     - **CI Integration:** Ensure all test suites run in CI (`ci.yml`) and fail the build on test failures.

## II. Documentation & Developer Experience

### 1. Enhanced Project Documentation
   - **Themed README.md:**
     - Rebuild `README.md` using `othneildrew/Best-README-Template` as a structural base.
     - Apply hand-drawn/sketchy styling using embedded HTML/CSS (if feasible and renders well on GitHub).
     - Content: Detailed project description, features, full tech stack overview, File System Access API usage (privacy benefits), PyScript interaction model, clear setup/build/run/test instructions, license.
   - **`ARCHITECTURE.md`:** Create a detailed document (or merge into README) covering:
     - Vue component hierarchy and data flow.
     - PyScript integration details (event system, `bleedy_interop.js`).
     - Strategy and current status of sketchy UI libraries.
   - **`LICENSE`:** Ensure MIT license file is present and correctly referenced.
   - **`CONTRIBUTING.md`:** Generate and customize guidelines for contributions.
   - **Inline Comments:** Continue to enhance comments for complex logic, public APIs of components/modules.

## III. UI/UX Refinements & Features

### 1. UI Consistency & Bug Fixing
   - Address any identified UI bugs, quirks, or inconsistencies (e.g., stepper button states, visual harmony between Element Plus and sketchy elements after sketchy library overhaul).
   - Ensure all interactive elements are highly responsive and provide clear feedback.

### 2. Accessibility (A11y)
   - Conduct a full A11y audit against WCAG guidelines.
   - Remediate all identified issues: keyboard navigation, focus states, ARIA attributes, color contrast, screen reader compatibility for all components, including custom/sketchy ones.

### 3. PWA (Progressive Web App)
   - Investigate feasibility and implement basic PWA features:
     - Web App Manifest.
     - Service Worker for caching assets and basic offline capabilities (app shell).
     - Refer to PyScript documentation on offline usage.

### 4. User-Facing Error Handling
   - Implement a system for clear, user-friendly, and thematically styled error messages for:
     - PyScript initialization failures.
     - Python processing errors.
     - File validation issues.
     - Network issues (if any parts become network-dependent).

### 5. File Handling Enhancements
   - **Image Previews:** Verify and enhance image previews in the `ImageSelection.vue` step.
   - **Advanced File Validation:**
     - Client-side: Prevent selection of non-image files more robustly.
     - Client-side: Detect and warn about animated GIFs (which might process unexpectedly).
     - Client-side: Warn about excessively large file sizes or too many files, suggesting potential performance issues.
   - **Session Persistence:**
     - Use File System Access API and IndexedDB to store `FileSystemFileHandle` objects of selected files.
     - Allow users to resume previous sessions or quickly re-select files.

### 6. Processing Enhancements
   - **Cancel Processing:** Implement a robust cancellation mechanism for ongoing image processing.
     - Define behavior: Cancel current image and continue? Cancel all remaining?
     - Ensure progress is correctly updated and potentially allow retry for skipped/failed images.

## IV. Future Feature Exploration (Longer Term)

These items require more research and design before implementation.

- **Advanced Bleed Options:**
  - Different bleed generation techniques (e.g., pixel stretch, content-aware fill via AI APIs, solid color).
  - Per-edge bleed amounts.
  - Intuitive unit conversions for bleed (mm, inches, pixels) based on target DPI.
- **Image Transformations:** Pre-bleed options like resize, crop.
- **Image Management:**
  - Deduplication of selected images.
  - OCR on filenames or image content for pattern recognition and auto-sorting/batching.
- **Technology Watch:**
  - Keep updated on new PyScript versions and features.
  - Monitor for new/better sketchy UI libraries or techniques.
  - Explore potential for AI-assisted image manipulation (e.g., generative fill for bleed).
  - Investigate further uses of the File System Access API (e.g., saving back to original file handle with permissions).

This list will be reviewed and prioritized as the project evolves.
