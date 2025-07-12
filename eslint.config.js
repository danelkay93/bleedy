import pluginVue from 'eslint-plugin-vue'
import {
  defineConfig,
  createConfig as vueTsEslintConfig,
} from '@vue/eslint-config-typescript'

export default defineConfig(
  pluginVue.configs['flat/recommended'],
  vueTsEslintConfig(),
)
