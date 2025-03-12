import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'
import 'doodle.css/doodle.css'

import App from './App.vue'
import router from './router'

import './assets/handdrawn.css'
import 'paper-css/paper.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus);

app.mount('#app')
