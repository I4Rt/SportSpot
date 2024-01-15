<template>
<!--  <change-pass-page-->
<!--    v-if="changePass"-->
<!--    @changePassword="change"-->
<!--  ></change-pass-page>-->
  <registration-page
      v-if="changePass"
      :selectFunction="selectFunction"
      @changePassword="changePass = false"
      @onLogout="$emit('onLogout')">
  </registration-page>
  <nav-bar
      :user="this.getUser"
      @changePassword="changePass = true"
      @showPage="viewPage"
      @onLogout="$emit('onLogout')"
      @openExplorer="openExplorer = true"
      ref="navBar">
  </nav-bar>
  <br>
  <calendar-page
      :selectFunction="selectFunction"
      @onLogout="$emit('onLogout')"
      v-if="page === 'Calendar'">
  </calendar-page>
  <cameras-page
      :selectFunction="selectFunction"
      @onLogout="$emit('onLogout')"
      v-if="page === 'Cameras'">
  </cameras-page>
  <rooms-page
      :selectFunction="selectFunction"
      @onLogout="$emit('onLogout')"
      v-if="page === 'Rooms'">
  </rooms-page>
  <explorer-page
      v-if="openExplorer"
      :openExplorer="openExplorer"
      :selectFunction="selectFunction"
      @closeExplorer="openExplorer = false"
      @openCalendar="$refs.navBar.showPage('Calendar'); openExplorer = false"
      ref="explorerPage">
  </explorer-page>
<!--  <explorer-page-->
<!--      v-if="page === 'Explorer'">-->
<!--  </explorer-page>-->

</template>

<script>
import NavBar from "@/components/NavBar";
import CalendarPage from "@/components/CalendarPage";
import CamerasPage from "@/components/CamerasPage";
import RoomsPage from "@/components/RoomsPage";
import ExplorerPage from "@/components/ExplorerPage";
import RegistrationPage from "@/components/RegistrationPage";
import {mapActions, mapGetters} from "vuex";

export default{
  props: ['refreshToken'],
  components: {
    NavBar,
    CalendarPage,
    CamerasPage,
    RoomsPage,
    ExplorerPage,
    RegistrationPage,
  },
    data() {
        return{
          changePass: false,
          page: 'Calendar',
          openExplorer: false,
        }
    },
  mounted() {
    this.selectFunction(this.getUserInfoFromDB)
  },
  computed:{
    ...mapGetters([
        'getUser'
    ])
  },
  methods: {
    change() {
      console.log('change')
    },
    viewPage(data) {
      this.page = data
      console.log(this.page + data)
    },
    async selectFunction(func, value){
      let respFunc
      if (arguments.length === 2) respFunc = await func(value)
      else respFunc = await func()
      console.log('selectFunction')
      // console.log(respFunc)
      try{
        if (respFunc.msg === 'Token has expired' || respFunc.msg === 'Bad token'){
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
    ...mapActions([
        'getUserInfoFromDB'
    ])
  }
}
</script>

<style>

</style>