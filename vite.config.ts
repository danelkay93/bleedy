import { defineConfig, optimizeDeps } from 'vite'
import vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import ElementPlus from 'unplugin-element-plus/vite'
import path from 'node:path'
import autoprefixer from 'autoprefixer';



export default defineConfig({
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
    '~/': `${path.resolve(__dirname, 'src')}/`,
    'vue': 'vue/dist/vue.esm-bundler.js'
  },
},
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('wired-')
        }
      }
    }),
    Components({
      resolvers: [
        ElementPlusResolver(),
        IconsResolver({
          prefix: 'Icon'
        })
      ]
    }),
    AutoImport({
      imports: ['vue', '@vueuse/core'],
      resolvers: [
        ElementPlusResolver(),
        IconsResolver({
          enabledCollections: ['ep']
        })
      ],
      vueTemplate: true
    }),
    Icons({
      autoInstall: true
    })
  ],
    css: {
    postcss: {
      plugins: [
        autoprefixer(),
      ],
    },
  },
  server: {
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp'
    }
  },
optimizeDeps: {
  include: [
    'element-plus',
    '@element-plus/icons-vue',
    'vue',
    'file-saver',
    'jszip'
  ]
},
ssr: {
  noExternal: ['element-plus'],
},
})
