# Project TODO List

## Sketchy UI Libraries Overhaul

**1. Fork `wired-elements` (High Priority):**
   - The currently used `wired-elements@3.0.0-rc.6` is old, and the original library appears unmaintained (last release 2018).
   - **Action:** Create an internal fork of `wired-elements` (e.g., under `vendor/bleedy-wired-elements` or as a private Git submodule/repository).
   - **Source:** Obtain the source code for `wired-elements@3.0.0-rc.6`.
   - **Integrate Patch:** Apply the existing `patches/wired-elements@3.0.0-rc.6.patch` to this fork.
   - **Audit & Update:**
     - Thoroughly audit all components within the fork that use `Rough.js` (especially those using fillers like `ZigZagFiller`).
     - Update these components to correctly use the API of the current `Rough.js` version (`4.6.6` or latest stable). The primary goal is to ensure all calls match `Rough.js`'s expected API (e.g., consistently using `fillPolygons` if that's the current standard in `Rough.js`).
     - This should eliminate the need for the `patches/roughjs@4.6.6.patch`.
   - **Dependencies:** Review and potentially update other dependencies of the forked `wired-elements` (e.g., Lit).
   - **Update Project Usage:** Modify `bleedy.py`'s `package.json` and imports to use this internal fork.

**2. Eliminate `Rough.js` Patch (Dependent on #1):**
   - Once the forked `wired-elements` correctly interfaces with `Rough.js`, the `patches/roughjs@4.6.6.patch` should no longer be necessary.
   - **Action:** Remove `patches/roughjs@4.6.6.patch` and its entry from `npm.patchedDependencies` in `package.json`.

**3. Verify and Address `DoodleCSS` and `paper-css`:**
   - **Action (Manual Check Needed):** Manually verify the maintenance status and stability of `DoodleCSS` and `paper-css`.
     - `DoodleCSS` (github.com/chr15m/DoodleCSS): Last commit appears to be ~2 years ago.
     - `paper-css`: Needs similar verification.
   - **Strategy:**
     - If deemed stable enough and causing no issues: Document their versions and keep them.
     - If problematic or very outdated:
       - Option A: Absorb their essential styles directly into the project's own SCSS/CSS structure.
       - Option B: Find actively maintained alternatives that provide a similar aesthetic.
       - Option C: Replicate the necessary effects using modern CSS or SVGs.

## PyScript Version Check Hook
- Fully implement and test the `scripts/check-pyscript-version.sh` script.
- Integrate with Husky as a pre-commit hook.
- Ensure the script correctly parses `index.html`, fetches the latest PyScript version, and handles the `.pyscript_version_ack` file logic.

## Architecture Documentation
- Create `ARCHITECTURE.md` detailing:
    - Vue component structure.
    - PyScript integration and JS-Python communication flow (current and planned improvements).
    - Data flow through the application.
    - Details about the sketchy UI libraries, the reasons for forking/patching, and the long-term strategy for them.
