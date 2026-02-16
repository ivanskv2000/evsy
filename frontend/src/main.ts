import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { installVueQuery } from './shared/plugins/vue-query'
import router from './router'
import './index.css'
import App from '@/App.vue'

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
installVueQuery(app)

app.mount('#app')
