<template>

  <!-- <search-page></search-page> -->
  <authorization-page v-if="!authorized && !registration" @sendLogin="onLogin" @registerUser="registration = true"></authorization-page>
  <registration-page v-if="!authorized && registration" @registrationCompleted="registration = false"></registration-page>
  <main-page v-else-if="authorized" @onLogout="authorized = false"></main-page>
  <!-- <my-component></my-component> -->
  <!-- <search-people></search-people>  -->
  <!-- <switch-displays-vue></switch-displays-vue> -->
</template>

<script>
import MainPage from './components/MainPage.vue';
import AuthorizationPage from "@/components/AuthorizationPage";
import RegistrationPage from "@/components/RegistrationPage";



// import bootstrap from 'bootstrap'
// import SearchPage from './components/SearchPage.vue'
// import SwitchDisplaysVue from './components/SwitchDisplays.vue'
// import MyComponent from './components/MyComponent.vue'
// import SearchPeople from './components/SearchPeople.vue'

export default {
  name: 'App',
  components: {
    AuthorizationPage,
    MainPage,
    RegistrationPage
  },
  data() {
    return{
      authorized: false,
      registration: false
    }
  },
  methods: {
    onLogin(data) {
      this.authorized = data
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
