<template>
 <div class="container nav-bar">
   <div class="row">
     <div class="col-2">
       <button
           class="btn"
           :class="page === 'Calendar' ? 'nav-bar-btn-on' : 'nav-bar-btn-off'"
           @click="showPage('Calendar')"
       >Календарь загруженности
       </button>
     </div>
     <div class="col-1">
       <button
           class="btn "
           :class="page === 'Cameras' ? 'nav-bar-btn-on' : 'nav-bar-btn-off'"
           @click="showPage('Cameras')">
         Настройка <br> камер
       </button>
     </div>
     <div class="col-2">
       <button
           class="btn "
           :class="page === 'Rooms' ? 'nav-bar-btn-on' : 'nav-bar-btn-off'"
           @click="showPage('Rooms')">
         Настройка помещений
       </button>
     </div>
     <div class="col-6">
       <div class="row justify-content-end">
         <div class="col-3">
           Пользователь
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script>
export default {
  name: "NavBar",
  data(){
    return{
      page: 'Calendar',
      isActive : false
    }
  },
  methods: {
    showPage(data){
      this.page = data
      this.$emit('showPage', data)
    }
  }
}
</script>

<style scoped>
.nav-bar{
  margin-top: 40px;
  /*background-color: #e8eae4;*/
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
}
.btn{
  font-size: 12px;
  font-weight: 700;
}
.nav-bar-btn-on{
  background-color: #29239f;
  color: aliceblue;
}
.nav-bar-btn-off:hover{
  background-color: rgba(243, 238, 238, 0.99);
}
.nav-bar-btn-off:focus{
  background-color: #29239f;
  color: aliceblue;
}

</style>