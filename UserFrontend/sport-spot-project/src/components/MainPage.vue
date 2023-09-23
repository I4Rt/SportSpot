<template>
<!--    Вы вошли-->
<!--    <button class="btn btn-primary" @click="$emit('logout')">Выйти</button>-->
  <nav-bar @showPage="viewPage" @onLogout="this.$emit('onLogout')"></nav-bar>
  <br>
  <calendar-page
      :selectFunction="selectFunction"
      @onLogout="this.$emit('onLogout')"
      v-if="page === 'Calendar'">
  </calendar-page>
  <cameras-page
      :selectFunction="selectFunction"
      @onLogout="this.$emit('onLogout')"
      v-if="page === 'Cameras'">
  </cameras-page>
  <rooms-page
      :selectFunction="selectFunction"
      @onLogout="this.$emit('onLogout')"
      v-if="page === 'Rooms'">
  </rooms-page>

</template>

<script>
import NavBar from "@/components/NavBar";
import CalendarPage from "@/components/CalendarPage";
import CamerasPage from "@/components/CamerasPage";
import RoomsPage from "@/components/RoomsPage";

export default{
  props: ['refreshToken'],
  components: {
    NavBar,
    CalendarPage,
    CamerasPage,
    RoomsPage
  },
    data() {
        return{
          page: 'Calendar'
        }
    },
  methods: {
    viewPage(data) {
      this.page = data
      console.log(this.page + data)
    },
    async selectFunction(func, value){
      let respFunc
      if (arguments.length === 2) respFunc = await func(value)
      else respFunc = await func()
      console.log(respFunc)
      try{
        if (respFunc.msg === 'Token has expired'){
          console.log('refresh')
          let refreshResp = await this.refreshToken()
          if (refreshResp.refresh === true) {
            if (arguments.length === 2) respFunc = await func(value)
            else respFunc = await func()
          }
          else this.$emit('onLogout')
        }
      }
      catch (err) {
        if (err.typeof === TypeError) console.log('')
      }
      return respFunc
    },
  }
}
</script>

<style>

</style>