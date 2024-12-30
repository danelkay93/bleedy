import { defineConfig, optimizeDeps } from 'vite'
import vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import ElementPlus from 'unplugin-element-plus/vite'
import path from 'node:path'



export default defineConfig({
resolve: {
  alias: {
    '~/': `${path.resolve(__dirname, 'src')}/`,
    'vue': 'vue/dist/vue.esm-bundler.js', // Add this line to alias Vue for runtime template compilation
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
  server: {
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp'
    }
  },
//       optimizeDeps:
// {
//   include: ['element-plus/**']
// }
    ssr: {
    // TODO: workaround until they support native ESM
    noExternal: ['element-plus'],
  },
})
