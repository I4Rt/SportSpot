import { createApp } from 'vue'
import App from './App.vue'
import store from './vuex/store.js'
import NewRegistration from './components/NewRegistation.vue'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
const app = createApp(App)
app.mount('#app')
app.use(store)
createApp(NewRegistration).mount('#newRegistration')
