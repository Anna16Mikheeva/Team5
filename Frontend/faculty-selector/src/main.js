import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import VueCookies from 'vue3-cookies'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(VueCookies, { expireTimes: '7d' })
app.mount('#app')
