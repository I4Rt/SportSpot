<template>
 <div class="container nav-bar">
   <div class="">
     <div class="grid-default">
       <div class="grid-default grid-default-main-buttons">
         <div class="">
           <button
               class="btn"
               :class="page === 'Calendar' ? 'nav-bar-btn-on' : 'nav-bar-btn-off'"
               @click="showPage('Calendar')"
           >Календарь <br> загруженности
           </button>
         </div>
         <div class="">
           <button
               class="btn "
               :class="page === 'Cameras' ? 'nav-bar-btn-on' : 'nav-bar-btn-off'"
               @click="showPage('Cameras')">
             Настройка <br> камер
           </button>
         </div>
         <div class="">
           <button
               class="btn "
               :class="page === 'Rooms' ? 'nav-bar-btn-on' : 'nav-bar-btn-off'"
               @click="showPage('Rooms')">
             Настройка <br> помещений
           </button>
         </div>
         <div class="">
           <button
               class="btn nav-bar-btn-off"
               @click="$emit('openExplorer')">
             Анализ <br> архивных данных
           </button>
         </div>
       </div>
         <div class="content content-end">
           <div class="dropdown">
             <div class="btn nav-bar-btn-off" >
               {{user.name}} <br> {{user.surname}}
               <div class="dropdown-menu">
                 <button @click="this.$emit('onLogout')" class="dropdown-item">Выйти</button>
                 <button @click="this.$emit('changePassword')" class="dropdown-item">Изменить пароль</button>
               </div>
             </div>
           </div>
         </div>
     </div>
   </div>
 </div>
</template>

<script>

export default {
  props: ['user'],
  emits: ['onLogout', 'showPage'],
  name: "NavBar",
  data(){
    return{
      page: 'Calendar',
      isActive : false,
      dropdownClass : '',
      authorized : this.getAuthorized
    }
  },
  methods: {
    showPage(data){
      this.page = data
      this.$emit('showPage', data)
    },
    // onLogout(){
    //   this.$store.state.authorized = false
    // }
  }
}
</script>

<style scoped lang="scss">
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
.btn:hover{
  background-color: #a1a1a1;
}

.dropdown:hover .dropdown-menu{
  display: block;
}
.dropdown-menu{
  display: none;
  margin: 0;
}
.dropdown-item:hover{
  background-color: #dadada;
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
.grid-default{
  display: grid;
  grid-gap: 50px;
  grid-template-columns: 60% 30%;
  &-main-buttons{
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 20px;
  }
}
.content{
  display: flex;
  align-items: center;
  &-center{
    justify-content: center;
  }
  &-end{
    justify-content: end;
  }
  &-start{
    justify-content: start;
  }
}

</style>