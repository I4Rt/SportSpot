<template>

  <!-- <search-page></search-page> -->
  <new-registation v-if="!autorization" @sendLogin="onLogin"></new-registation>
  
  <main-page v-else-if="autorization" @logout="showLoginPage"></main-page>
  <!-- <my-component></my-component> -->
  <!-- <search-people></search-people>  -->
  <!-- <switch-displays-vue></switch-displays-vue> -->
</template>

<script>
import NewRegistation from './components/NewRegistation.vue'
import MainPage from './components/MainPage.vue';

// import bootstrap from 'bootstrap'
// import SearchPage from './components/SearchPage.vue'
// import SwitchDisplaysVue from './components/SwitchDisplays.vue'
// import MyComponent from './components/MyComponent.vue'
// import SearchPeople from './components/SearchPeople.vue'

export default {
  name: 'App',
  components: {
    // SearchPeople
    NewRegistation,
    MainPage
  },
  data() {
    return{
      autorization: false
    }
  },
  methods: {
    showMainPage(authorize) {
      this.autorization = authorize

    },
    showLoginPage() {
      console.log('logout')
      this.autorization = false
    },
    onLogin(data) {
      this.autorization = data
    }
  }
}
</script>

<style>


/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
