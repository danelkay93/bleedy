// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// import './assets/index.scss';  // Import your custom theme overrides


import App from './App.vue'
import router from './router'

// Import Element Plus CSS
import 'element-plus/dist/index.css';
import 'doodle.css/doodle.css';
import 'wired-elements';
import './assets/handdrawn.css'
import 'paper-css/paper.css'

const app = createApp(App)

// Tell Vue to ignore custom elements starting with 'wired-'
app.config.compilerOptions.isCustomElement = (tag) => tag.startsWith('wired-');

app.use(createPinia())
app.use(router)


app.mount('#app')
