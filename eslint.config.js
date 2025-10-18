import pluginVue from 'eslint-plugin-vue'
import {defineConfig, createConfig as vueTsEslintConfig} from '@vue/eslint-config-typescript'

export default defineConfig(
  {
    ignores: [
      '**/dist/**',
      '**/dist-ssr/**',
      '**/coverage/**',
      'auto-imports.d.ts',
      'components.d.ts',
      '**/*.d.ts',
      'node_modules/**'
    ]
  },
  pluginVue.configs['flat/recommended'],
  vueTsEslintConfig()
)
