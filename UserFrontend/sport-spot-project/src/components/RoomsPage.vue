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
          <form @submit.prevent="selectFunction(save)" style="margin-top: 10px">
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
              <input class="input-field" type="text" v-model.trim="room.classId"
                     :class="v$.room.classId.$error ? 'is-invalid' : ''">
              <p v-if="v$.room.classId.$dirty && v$.room.classId.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group" >
              <button type="submit" class="btn btn-success" >Сохранить</button>
            </div>
          </form>
          <button
              class="btn btn-primary"
              @click="removeRoom(room.id); resetRoom()"
              style="position: absolute; top: 0; right: 0; margin-right: 15px; margin-top: 116px">
            Удалить
          </button>

          <label style="font-weight: 700">Сектора</label>
          <div class="row" v-if="roomSelected">
            <div class="col-6">
              <label>Назначенные</label>
              <table class="window linear-table">
                <tr  v-for="(camera, index) in getUsedCameras" :key="index">
                  <td style="width: 200px" >
                    <span style="margin-left: 5px">{{ camera.name }}</span>
                    <table>
                      <tr v-for="(sector, index) in camera.sectors" :key="index">
                        <td>
                          <span style="margin-left: 20px">{{ sector.name }}</span>
                          <button class="hidden-button swipe-sector" @click="selectFunction(removeSectorFromRoom,sector)">
                            <img :src="require('../assets/icons/arrow-right.png')" alt="">
                          </button>
                          <button class="hidden-button show-close-sector" @click="chooseSector(sector)">
                            <img :src="require('../assets/icons/eye-closed.png')" alt="">
                          </button>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </div>
            <div class="col-6">
              <label>Существующие</label>
              <table class="window linear-table" >
                <tr v-for="(camera, index) in getUnusedCameras" :key="index">
                  <td style="width: 200px" >
                    <span style="margin-left: 5px">{{ camera.name }}</span>
                    <table>
                      <tr v-for="(sector, index) in camera.sectors" :key="index">
                        <td>
                          <span style="margin-left: 20px">{{ sector.name }}</span>
                          <button class="hidden-button swipe-sector" @click="selectFunction(setSectorToRoom,sector)">
                            <img :src="require('../assets/icons/arrow-left.png')" alt="">
                          </button>
                          <button class="hidden-button show-close-sector" @click="chooseSector(sector)">
                            <img :src="require('../assets/icons/eye-closed.png')" alt="">
                          </button>
                        </td>
                      </tr>
                    </table>
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
            <!--            <img src="http://localhost:5000/videoStream" style="width: 100%">-->
            <img :src="require('../assets/images/img1.png')" style="width: 100%" alt="img1">
            <p>Информация сектора</p>
            <p>Сектор {{sector.name}}</p>
            <span>Техническая информация:</span>
            <ul>
              <li>Границы:</li>
              <li>Высота от пола:</li>
              <li>Тип сектора: <span v-if="sectorSelected">{{getSectorTypeByID(sector.typeId).name}}</span></li>
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
        id: null,
        classId: null,
        name: '',
        sportObjectId: '',
        roomType: {
          id: null,
          name: ''
        }
      },
      sector: {
        camId: null,
        id: null,
        name: '',
        points: [],
        roomId: null,
        typeId: null,
      },
      roomSelected: false,
      sectorSelected: false
    }
  },
  validations: {
    room: {
      name: {required},
      classId: {required}
    }
  },
  computed: {
    ...mapGetters([
        'getRooms',
        'getRoomByID',
        'getUsedCameras',
        'getUnusedCameras',
        'getSectorByID',
        'getSectorTypeByID',
        'getSectorTypes'
    ]),
  },
  mounted() {
    if (this.getRooms.length === 0){
      this.selectFunction(this.getRoomsFromDB)
    }
    if (this.getSectorTypes.length === 0){
      this.selectFunction(this.getSectorTypesFromDB)
    }
  },
  methods: {
    save() {
      this.v$.room.$touch()
      let returnResult
      if (!this.v$.room.$error) {
        console.log('Валидация прошла успешно')
        returnResult = fetch('http://localhost:5000/setRoom', {
          credentials: "include",
          method: 'POST',
          cors: 'no-cors',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
          },
          body: JSON.stringify({
            "classId": this.room.classId,
            "name": this.room.name,
            "id": null,
          })
          })
            .then(response => response.json())
            .then((response) => {
              console.log(response)
              this.room.id = response.id
              console.log(this.$store.commit('setRooms', Object.assign({}, this.room)))
              this.v$.room.$reset()
              return response
            });
      }
      else console.log('Валидация не прошла')
      return returnResult
    },
    getSectorTypesFromDB() {
      return fetch(`http://localhost:5000/getSectorTypes`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log('sectorTypes ')
            this.$store.state.sectorTypes = response
            console.log(this.$store.state.sectorTypes)
            return response
          });
    },
    getUnusedCameraSectorsByRoomIdFromDB() {
      return fetch(`http://localhost:5000/getUnusedCameraSectorsByRoomId?roomId=${this.room.id}`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log('unused rooms ')
            console.log(response)
            this.$store.state.unusedCameras = response
            console.log(this.getUnusedCameras)
            return response
          });
    },
    getUsedCameraSectorsByRoomIdFromDB() {
      return fetch(`http://localhost:5000/getCameraSectorsByRoomId?roomId=${this.room.id}`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.$store.state.usedCameras = response
            return response
          });
    },
    getRoomsFromDB() {
      return fetch('http://localhost:5000/getRooms', {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.$store.state.rooms = response
            return response
          });
    },
    chooseRoom(room) {
      console.log(room.id)
      this.room = this.getRoomByID(room.id)
      this.roomSelected = true
      this.reloadCameraSectors()
      this.resetSector()
    },
    chooseSector(sector) {
      console.log(sector)
      console.log(sector.id)
      this.sector = sector
      this.sectorSelected = true
    },
    resetRoom(){
      let roomCopy = Object.assign({}, this.room)
      this.room = roomCopy
      this.room.name = ''
      this.room.classId = null
      this.room.id = null
      this.room.sportObjectId = ''
      this.room.roomType = {
        id: null,
        name: ''
      }
      this.$store.state.unusedCameras = {}
      this.$store.state.usedCameras = {}
      this.resetSector()
    },
    resetSector() {
      this.sector.camId = null
      this.sector.id = null
      this.sector.name = ''
      this.sector.points = []
      this.sector.roomId = null
      this.sector.typeId = null
      this.sectorSelected = false
    },
    reloadCameraSectors() {
      this.selectFunction(this.getUsedCameraSectorsByRoomIdFromDB)
      this.selectFunction(this.getUnusedCameraSectorsByRoomIdFromDB)
    },
    setSectorToRoom(sector){
      return fetch(`http://localhost:5000/setSectorToRoom?sectorId=${sector.id}&roomId=${this.room.id}`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.reloadCameraSectors()
            return response
          });
    },
    removeSectorFromRoom(sector){
      return fetch(`http://localhost:5000/removeSectorFromRoomLsit?sectorId=${sector.id}&roomId=${this.room.id}`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.reloadCameraSectors()
            return response
          });
    },
    selectFunction(func, value){
      let respFunc
      if (arguments.length === 2) respFunc = func(value)
      else respFunc = func()
      let refresh
      console.log('respFunc ' + respFunc)
      if (respFunc === "Bad token") {
        refresh = this.refreshToken()
        if (refresh === "ok"){
          console.log('refreshOk')
          respFunc = func()
        }
        if (respFunc === "Bad token") alert('logout pls')
      }
      else return respFunc
    },
    ...mapActions([
        'addRoom',
        'removeRoom',
        'refreshToken'
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
.hidden-button:hover{
  background-color: #dadada;
  cursor: pointer;
}
.window{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
}
.camera:hover{
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
.linear-table{
  background: linear-gradient(#dfe0ff 50%, #ffffff 50%);
  background-size: 100% 52px;
}

</style>