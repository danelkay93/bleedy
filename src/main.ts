// import './assets/main.css'

import { createApp } from 'vue'
import ElementPlus from 'element-plus';
// import 'element-plus/lib/theme-chalk/index.css';
import 'doodle.css/doodle.css';
import { createPinia } from 'pinia'

// import './assets/index.scss';  // Import your custom theme overrides


import App from './App.vue'
import router from './router'

// Import Element Plus CSS
// import 'element-plus/dist/index.css';
import 'wired-elements';
import './assets/handdrawn.css'
import 'paper-css/paper.css'

const app = createApp(App)


app.use(createPinia())
app.use(router)
app.use(ElementPlus);


app.mount('#app')
