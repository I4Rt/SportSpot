<template>

  <!-- <search-page></search-page> -->
  <authorization-page v-if="!authorized && !registration" @sendLogin="onLogin"></authorization-page>
<!--  <registration-page v-if="!authorized && registration" @registrationCompleted="registration = false"></registration-page>-->
  <main-page
      :refreshToken="refreshToken"
      v-else-if="authorized"
      @onLogout="onLogout">
  </main-page>
  <!-- <my-component></my-component> -->
  <!-- <search-people></search-people>  -->
  <!-- <switch-displays-vue></switch-displays-vue> -->
</template>

<script>
import MainPage from './components/MainPage.vue';
import AuthorizationPage from "@/components/AuthorizationPage";


export default {
  emits: ['onLogout'],
  name: 'App',
  components: {
    AuthorizationPage,
    MainPage,
  },
  data() {
    return{
      authorized: false,
    }
  },
  mounted() {
    this.checkRefresh()
  },
  methods: {
    onLogout() {
      console.log('logout')
      this.authorized = false
      fetch('http://localhost:5000/logout',{
        method: 'GET',
        credentials: 'include',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      }).then(response => response.json())
          .then(response => {
            console.log(response)
          })
    },
    onLogin(data) {
      this.authorized = data
    },
    async checkRefresh(){
      console.log('checkRefresh')
      let refreshResp = await this.refreshToken()
      try{
        if (refreshResp.refresh === true) this.authorized = true
      } catch (err) {
        console.log(err)
      }
    },
    async refreshToken(){
      let returnResult
      try {
        returnResult = await fetch('http://localhost:5000/refresh', {
          method: 'POST',
          credentials:"include",
          cors: 'no-cors',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
          },
        })
            .then(response => response.json())
            .then(response => {
              return response
            })
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
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
