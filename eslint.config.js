/* global module, process */
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser', // Support for TypeScript
    ecmaVersion: 2021,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended', // Best practices for Vue 3
    'plugin:@typescript-eslint/recommended', // TypeScript support
    'prettier' // Prettier integration
  ],
  plugins: ['vue', '@typescript-eslint'],
  rules: {
    // Custom rules
    'vue/multi-word-component-names': 'off', // Disable multi-word component name rule for Vue 3
    'no-unused-vars': 'off', // Delegate unused vars to TypeScript
    '@typescript-eslint/no-unused-vars': ['warn'], // Enable unused vars with TypeScript
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  },
  overrides: [
    {
      files: ['*.ts', '*.tsx'],
      rules: {
        // TypeScript-specific rules can go here
      }
    }
  ]
};