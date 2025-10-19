import pluginVue from 'eslint-plugin-vue'
import {defineConfig, createConfig as vueTsEslintConfig} from '@vue/eslint-config-typescript'

export default defineConfig(
  {
    ignores: ['dist/**', 'dist-ssr/**', 'node_modules/**', 'auto-imports.d.ts', 'components.d.ts']
  },
  pluginVue.configs['flat/recommended'],
  vueTsEslintConfig()
)
