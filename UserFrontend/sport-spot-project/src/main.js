import { createApp } from 'vue'
import App from './App.vue'
import store from './vuex/store.js'
import NewRegistration from './components/NewRegistation.vue'
const app = createApp(App)
app.mount('#app')
app.use(store)
createApp(NewRegistration).mount('#newRegistration')
