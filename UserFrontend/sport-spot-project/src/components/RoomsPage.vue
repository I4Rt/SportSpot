<template>
  <div>
    <div class="container" >
      <div class="row justify-content-around">
        <div class="col-3">
          <div class="row">
            <label class="field">Помещения</label>
            <button id="add" style="margin-top: 5px" @click="resetRoom">Добавить</button>
          </div>
        </div>
        <div class="col-4">
          <label class="field">Добавить</label>
        </div>
        <div class="col-5">
          <label class="field">Просмотр</label>
        </div>
        <div class="col-3" >
          <div class="row window camera col-12" @click="chooseRoom(room)" v-for="(room, index) in getRooms"
               :key="index">
            <span class="room-name">{{room.name}}</span>
          </div>
        </div>

        <div class="col-4 window">
          <label style="font-weight: 700; margin-top: 10px">Помещение</label>
          <form @submit.prevent="save" style="margin-top: 10px">
            <div class="">
              <label> Название: </label>
              <input class=" input-field" type="text" v-model.trim="room.name"
                     :class="v$.room.name.$error ? 'is-invalid' : ''" >
              <p v-if="v$.room.name.$dirty && v$.room.name.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> Класс помещения: </label>
              <input class="input-field" type="text" v-model.trim="room.class"
                     :class="v$.room.class.$error ? 'is-invalid' : ''">
              <p v-if="v$.room.class.$dirty && v$.room.class.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group" >
              <button type="submit" class="btn btn-primary" >Сохранить</button>
            </div>
          </form>
          <label style="font-weight: 700">Сектора</label>
          <div class="row" v-if="roomSelected">
            <div class="col-6">
              <label>Назначенные</label>
              <table class="window">
                <tr  v-for="(camera, index) in getCamerasByRoomID(room.id)" :key="index">
                  <td style="width: 200px" >
                    <span style="margin-left: 5px">{{ camera.name }}</span>
                    <button class="hidden-button swipe-sector" @click="deleteCameraFromRoom(camera)">
                      <img :src="require('../assets/icons/arrow-right.png')" alt="">
                    </button>
                    <button class="hidden-button show-close-sector">
                      <img :src="require('../assets/icons/eye-closed.png')" alt="">
                    </button>
                  </td>
                </tr>
              </table>
            </div>
            <div class="col-6">
              <label>Существующие</label>
              <table class="window" >
                <tr v-for="(camera, index) in getCamerasWithoutRoomID" :key="index">
                  <td style="width: 200px" >
                    <span style="margin-left: 5px">{{ camera.name }}</span>
                    <tr v-for="(sector, index) in camera.sectors" :key="index">
                      <td>
                        <span style="margin-left: 5px">{{ sector.name }}</span>
                        <button class="hidden-button swipe-sector" @click="addCameraToRoom(camera)">
                          <img :src="require('../assets/icons/arrow-left.png')" alt="">
                        </button>
                        <button class="hidden-button show-close-sector">
                          <img :src="require('../assets/icons/eye-closed.png')" alt="">
                        </button>
                      </td>
                    </tr>
                  </td>
                </tr>
              </table>
            </div>
          </div>
          <p v-else style="font-size: 15px">Выберите помещение для отображение секторов</p>
          <br>
        </div>
        <div class="col-5">
          <div class="col-12 window">
            <p>Изображение</p>
            <p>Информация сектора</p>
            <p>Сектор</p>
            <span>Техническая информация:</span>
            <ul>
              <li>Границы:</li>
              <li>Высота от пола:</li>
              <li>Тип сектора: <span v-if="roomSelected"></span></li>
            </ul>
            <p>Справка:</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import {mapActions} from 'vuex'
import { useVuelidate } from '@vuelidate/core'
import { required} from '@vuelidate/validators'

export default {
  name: "RoomsPage",
  setup () {
    return {
      v$: useVuelidate()
    }
  },
  data(){
    return {
      room: {
        id: -1,
        camID: [],
        name: '',
        class: ''
      },
      count: 0,
      roomSelected: false
    }
  },
  validations: {
    room: {
      name: {required},
      class: {required}
    }
  },
  computed: {
    ...mapGetters([
        'getRooms',
        'getRoomByID',
        'getCameras',
        'getCamerasByRoomID',
        'getCamerasWithoutRoomID',
        'getRoomCount'
    ]),
  },
  methods: {
    save() {
      this.v$.room.$touch()
      if (!this.v$.room.$error) {
        console.log('Валидация прошла успешно')
        this.room.id = this.getRoomCount
        this.addRoomCount(this.getRoomCount+1)
        let roomCopy = Object.assign({}, this.room)
        this.addRoom(roomCopy)
        this.v$.room.$reset()
      }
      else console.log('Валидация не прошла')
    },
    chooseRoom(room) {
      console.log(room.id)
      this.room = this.getRoomByID(room.id)
      this.roomSelected = true
    },
    resetRoom(){
      let roomCopy = Object.assign({}, this.room)
      this.room = roomCopy
      this.room.name = ''
      this.room.class = ''
    },
    addCameraToRoom(camera){
      console.log("camera-room-id" + camera.roomID)
      camera.roomID = this.room.id
    },
    deleteCameraFromRoom(camera){
      camera.roomID = -1
    },
    ...mapActions([
        'addRoom',
        'addRoomCount'
    ])
  }
}
</script>

<style scoped>
#add{
  width: 110px;
  /*height: 35px;*/
  position: absolute;
  right: 0;
  top: 0;
  margin-right: 30px;
  border-radius: 10px;
  font-size: 18px;
}
.swipe-sector{
  position: absolute;
  right: 0;
  margin-right: 45px;
  margin-bottom: 5px;
}
.show-close-sector{
  position: absolute;
  right: 0;
  margin-right: 20px;
}
.hidden-button{
  background: inherit;
  border: none;
  width: 25px;
  /*vertical-align: center;*/
}
.window{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
}
.camera:hover{
  background-color: #dadada;
  cursor: pointer;
}
.hidden-button:hover{
  background-color: #dadada;
  cursor: pointer;
}
.field {
  font-size: 22px;
  font-weight: 700;
}
.room-name{
  font-size: 14px;
  font-weight: 500;
  margin: 7px;
}
.input-field{
  outline: none;
  width: 200px;
  height: 25px;
  font-size: 14px;
  position: absolute;
  right: 0;
  margin-right: 15px;
  border-radius: 5px ;
  border: 1px solid grey;
}
tr:nth-child(even) {
  background: #dfe0ff;
}

</style>