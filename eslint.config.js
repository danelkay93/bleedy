import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import eslintConfigPrettier from "eslint-config-prettier"; // To disable ESLint rules that conflict with Prettier

export default [
  // Global ignores
  {
    ignores: ["dist/**", "node_modules/**", "*.d.ts", "public/**"],
  },
  // ESLint recommended base
  pluginJs.configs.recommended,

  // TypeScript configuration
  // This applies to .ts, .tsx, .mts, .cts files by default through tseslint.config
  ...tseslint.config({
    files: ["**/*.{js,jsx,mjs,cjs,ts,tsx,vue}"], // Apply TS parsing broadly, Vue files handled below
    extends: [
      ...tseslint.configs.recommended,
      // ...tseslint.configs.recommendedTypeChecked, // Optional: for rules requiring type info
    ],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: 2021,
        sourceType: "module",
        // project: true, // Automatically finds tsconfig.json
        // tsconfigRootDir: import.meta.dirname, // For monorepos or specific setups
      },
    },
    rules: {
        '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
        // Add any other TypeScript specific overrides here
    }
  }),

  // Vue 3 configuration
  ...pluginVue.configs['flat/vue3-recommended'],
  {
    files: ["**/*.vue"], // Target only Vue files for Vue-specific parsing and rules
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
      // The parser for .vue files is vue-eslint-parser, which should be set by pluginVue.configs
      // It then uses the TypeScript parser internally for <script lang="ts"> blocks.
    },
    rules: {
      'vue/multi-word-component-names': 'off',
      // Add any other Vue specific overrides here
    }
  },

  // General project-specific rules (applied to JS, TS, Vue files)
  {
    files: ["src/**/*.{js,jsx,mjs,cjs,ts,tsx,vue}"], // Apply to src files
    rules: {
      'no-unused-vars': 'off', // Disabled in favor of @typescript-eslint/no-unused-vars
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      // Add other global project rules here
    },
  },

  // Prettier compatibility: Must be last to override other formatting rules from other configs.
  eslintConfigPrettier,
];
