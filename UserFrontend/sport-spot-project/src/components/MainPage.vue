<template>
<!--    Вы вошли-->
<!--    <button class="btn btn-primary" @click="$emit('logout')">Выйти</button>-->
  <nav-bar @showPage="viewPage" @onLogout="this.$emit('onLogout')"></nav-bar>
  <br>
  <calendar-page v-if="page === 'Calendar'"></calendar-page>
  <cameras-page v-if="page === 'Cameras'"></cameras-page>
  <rooms-page v-if="page === 'Rooms'"></rooms-page>

</template>

<script>
import NavBar from "@/components/NavBar";
import CalendarPage from "@/components/CalendarPage";
import CamerasPage from "@/components/CamerasPage";
import RoomsPage from "@/components/RoomsPage";

export default{
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
  }
}
</script>

<style>

</style>