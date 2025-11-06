#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import process from 'node:process';

const args = process.argv.slice(2);
const flagSet = new Set();
const passthroughArgs = [];

/**
 * Parse a string into arguments, respecting quoted substrings.
 * Handles both single and double quotes.
 * @param {string} str - The string to parse
 * @returns {string[]} Array of parsed arguments
 */
function parseQuotedArgs(str) {
  const result = [];
  let current = '';
  let inQuote = null;
  
  for (let i = 0; i < str.length; i++) {
    const char = str[i];
    
    if (inQuote) {
      if (char === inQuote) {
        inQuote = null;
      } else {
        current += char;
      }
    } else if (char === '"' || char === "'") {
      inQuote = char;
    } else if (char === ' ') {
      if (current) {
        result.push(current);
        current = '';
      }
    } else {
      current += char;
    }
  }
  
  if (current) {
    result.push(current);
  }
  
  return result;
}

for (const arg of args) {
  if (arg === '--help' || arg === '-h') {
    printHelp();
    process.exit(0);
  }
  if (arg.startsWith('--test-args=')) {
    const argsString = arg.replace('--test-args=', '');
    passthroughArgs.push(...parseQuotedArgs(argsString));
    continue;
  }
  if (arg === '--with-typecheck' || arg === '--skip-tests' || arg === '--skip-build' || arg === '--skip-lint') {
    flagSet.add(arg);
    continue;
  }
  console.error(`Unknown option: ${arg}`);
  printHelp();
  process.exit(1);
}

const steps = [];

if (!flagSet.has('--skip-lint')) {
  steps.push({
    key: 'lint',
    label: 'ESLint',
    command: 'npm',
    commandArgs: ['run', 'lint'],
    description: 'Static analysis via ESLint',
  });
}

if (flagSet.has('--with-typecheck')) {
  steps.push({
    key: 'typecheck',
    label: 'Vue Type Check',
    command: 'npm',
    commandArgs: ['run', 'type-check'],
    description: 'Full vue-tsc type checking (may fail due to known issues)',
  });
}

if (!flagSet.has('--skip-build')) {
  steps.push({
    key: 'build',
    label: 'Vite Build',
    command: 'npm',
    commandArgs: ['run', 'build'],
    description: 'Production build via Vite',
  });
}

if (!flagSet.has('--skip-tests')) {
  const testArgs = passthroughArgs.length > 0 ? ['--', ...passthroughArgs] : ['--', '--run'];
  if (!testArgs.includes('--passWithNoTests')) {
    testArgs.push('--passWithNoTests');
  }
  steps.push({
    key: 'tests',
    label: 'Vitest',
    command: 'npm',
    commandArgs: ['run', 'test:unit', ...testArgs],
    description: 'Unit tests with Vitest',
  });
}

if (steps.length === 0) {
  console.log('No steps selected. Use --help for usage information.');
  process.exit(0);
}

console.log('🔧  Running Bleedy agent environment checks...');

for (const step of steps) {
  console.log(`\n➡️  ${step.label} – ${step.description}`);
  const result = spawnSync(step.command, step.commandArgs, {
    stdio: 'inherit',
    shell: process.platform === 'win32',
  });

  if (result.status !== 0) {
    console.error(`\n❌  ${step.label} failed. See output above.`);
    process.exit(typeof result.status === 'number' ? result.status : 1);
  }
}

console.log('\n✅  All selected checks passed!');

function printHelp() {
  console.log(`Bleedy Agent QA Helper\n\nUsage: npm run qa [options]\n\nOptions:\n  --with-typecheck   Include the slower vue-tsc type checking step\n  --skip-lint        Skip the ESLint run\n  --skip-build       Skip the Vite production build\n  --skip-tests       Skip the Vitest suite\n  --test-args=<...>  Pass additional arguments directly to Vitest\n  -h, --help         Show this help message\n\nExamples:\n  npm run qa\n  npm run qa -- --with-typecheck\n  npm run qa -- --skip-tests\n  npm run qa -- --test-args='--run --coverage'\n`);
}
