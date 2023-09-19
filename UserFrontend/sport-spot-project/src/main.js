import { createApp } from 'vue'
import App from './App.vue'
import store from './vuex/store.js'
import NewRegistration from './components/AuthorizationPage.vue'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'

// import bootstrap from 'bootstrap/dist/js/bootstrap.js'
const app = createApp(App)
app.mount('#app')
app.use(store)
createApp(NewRegistration).mount('#newRegistration')
