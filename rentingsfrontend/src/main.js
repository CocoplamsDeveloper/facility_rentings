import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'
import axios from 'axios'

createApp(App).use(router).mount('#app')
