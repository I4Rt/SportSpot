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
              <select v-model="room.classId" class="input-field">
                <option v-for="(roomType, index) in getRoomTypes" :value="roomType.id" :key="index">
                  {{roomType.name}}
                </option>
              </select>
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
              <div id="table-used" class="window linear-table">
                <table >
                  <tr  v-for="(camera, index) in getUsedCameras" :key="index">
                    <td style="width: 200px" >
                      <span style="margin-left: 5px">{{ camera.name }}</span>
                      <table>
                        <tr v-for="(cameraSector, index) in camera.sectors" :key="index" >
                          <td style="padding: 0">
                            <div class="grid-default" style="height: 26px">
                              <div style="margin-left: 20px">
                                <span >{{ cameraSector.name }}</span>
                              </div>
                              <div class="content content-end">
                                <button class="hidden-button swipe-sector" @click="selectFunction(removeSectorFromRoom,cameraSector)">
                                  <img :src="require('../assets/icons/arrow-right.png')" alt="">
                                </button>
                                <button class="hidden-button show-close-sector" @click="chooseSector(cameraSector)">
                                  <img v-if="sectorSelected && sector.id === cameraSector.id" style="margin-bottom: 5px" :src="require('../assets/icons/eye-opened.png')" alt="">
                                  <img v-else style="margin-bottom: 5px" :src="require('../assets/icons/eye-closed.png')" alt="">
                                </button>
                              </div>
                            </div>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </div>
            </div>
            <div class="col-6">
              <label>Существующие</label>
              <div id="table-unused" class="window linear-table">
                <table >
                  <tr v-for="(camera, index) in getUnusedCameras" :key="index">
                    <td style="width: 200px" >
                      <span style="margin-left: 5px">{{ camera.name }}</span>
                      <table>
                        <tr v-for="(cameraSector, index) in camera.sectors" :key="index" >
                          <td style="padding: 0">
                            <div id="td-height" class="grid-default" style="height: 26px">
                              <div style="margin-left: 20px">
                                <span class="sector-name" :title="cameraSector.name">{{ cameraSector.name }}</span>
                              </div>
                              <div class="content content-end">
                                <button class="hidden-button swipe-sector" @click="selectFunction(setSectorToRoom,cameraSector)">
                                  <img :src="require('../assets/icons/arrow-left.png')" alt="">
                                </button>
                                <button class="hidden-button show-close-sector" @click="chooseSector(cameraSector)">
                                  <img
                                      v-if="sectorSelected && sector.id === cameraSector.id"
                                      style="margin-bottom: 5px"
                                      :src="require('../assets/icons/eye-opened.png')"
                                      alt="">
                                  <img
                                      v-else style="margin-bottom: 5px"
                                      :src="require('../assets/icons/eye-closed.png')"
                                      alt="">
                                </button>
                              </div>
                            </div>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </div>
            </div>
          </div>
          <p v-else style="font-size: 15px">Выберите помещение для отображение секторов</p>
          <br>
        </div>
        <div class="col-5">
          <show-camera
              :cameraID="sector.camId"
              :sector="sector"
              :selectFunction="selectFunction"
              :sectorSelected=sectorSelected
              :cameraSelected="sectorSelected"
              :save="save"
              @pushSectorPoints="(data) => this.sector.points.push(data)"
              @removeSectorPoints="this.sector.points = []"
              ref="showCamera"
          ></show-camera>
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
import ShowCamera from "@/components/ShowCamera";

export default {
  props: ['selectFunction'],
  name: "RoomsPage",
  components: {
    ShowCamera
  },
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
        // roomType: {
        //   id: null,
        //   name: ''
        // }
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
        'getSectorTypes',
        'getSectorsByCameraID',
        "getRefreshInterval",
        'getRoomTypes'

    ])
  },
  mounted() {
    if (this.getRefreshInterval){
      console.log('clean')
      this.$store.commit('clearRefreshInterval')
    }
    this.selectFunction(this.getRoomsFromDB)
    this.selectFunction(this.getSectorTypesFromDB)
    this.selectFunction(this.getRoomTypesFromDB)
    this.resetRoom()
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
            "id": this.room.id,
          })
          })
            .then(response => response.json())
            .then((response) => {
              console.log(response)
              this.room.id = response.id
              if (this.getRoomByID(response.id) === undefined) {
                this.addRoom(Object.assign({}, this.room))
                console.log('yesCheck')
              }
              this.v$.room.$reset()
              if (this.sector.camId !== null) this.selectFunction(this.setSector, this.sector)
              return response
            });
      }
      else console.log('Валидация не прошла')
      return returnResult
    },
    async setSector(sector){
      console.log('1 sector ' + sector)
      let returnValue
      try {
        returnValue = await fetch('http://localhost:5000/setSector', {
          credentials: "include",
          method: 'POST',
          cors: 'no-cors',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
          },
          body: JSON.stringify({
            "camId": sector.camId,
            "id": sector.id,
            "name": sector.name,
            "points": sector.points,
            "roomId": sector.roomId,
            "typeId": sector.typeId
          })
        })
            .then(response => response.json())
            .then((response) =>{
              sector.id = response.id
              if (sector.id === null) return  response
              else return sector
            })
      } catch (err) {
        console.error(err)
      }
      return returnValue
    },
    async getUnusedCameraSectorsByRoomIdFromDB() {
      return await fetch(`http://localhost:5000/getUnusedCameraSectorsByRoomId?roomId=${this.room.id}`, {
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
    async getUsedCameraSectorsByRoomIdFromDB() {
      return await fetch(`http://localhost:5000/getCameraSectorsByRoomId?roomId=${this.room.id}`, {
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
    async chooseSector(cameraSector) {
      console.log('cameraSector')
      console.log(cameraSector)
        let camId = cameraSector.camId
        this.selectFunction(this.getSectorsByCameraIDFromDB, camId).then(() => {
          this.showSector(cameraSector)
        })
    },
    showSector(cameraSector) {
      if (this.sector.id === cameraSector.id) this.resetSector()
      else{
        let lastCamId = this.sector.camId
        this.sector = this.getSectorByID(cameraSector.id)
        this.sectorSelected = true
        this.$refs.showCamera.drawClear()
        let interval = setInterval(() => {
          if (this.sector.id === cameraSector.id){
            if (lastCamId !== cameraSector.camId){
              this.$refs.showCamera.changeImgPath("data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=").then(
                  () => {
                    this.$refs.showCamera.drawImage()
                  })
            }
            if (this.sector.points.length !== 0) {
              this.$refs.showCamera.drawSectorPoints()
            }
            clearInterval(interval)
          }
        }, 100)
      }
    },
    resetRoom(){
      let roomCopy = Object.assign({}, this.room)
      this.room = roomCopy
      this.room.name = ''
      this.room.classId = null
      this.room.id = null
      this.room.sportObjectId = ''
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
      this.$refs.showCamera.drawClear()
      if (this.getRefreshInterval){
        console.log('clean')
        this.$store.commit('clearRefreshInterval')
      }
    },
    reloadCameraSectors() {
      this.selectFunction(this.getUsedCameraSectorsByRoomIdFromDB)
      this.selectFunction(this.getUnusedCameraSectorsByRoomIdFromDB).then(() => {
        let tdHeight = document.getElementById("td-height").offsetHeight
        let linearTable = document.getElementsByClassName('linear-table')
        Array.from(linearTable).forEach((item) => {
          item.style.setProperty('--td-height', `${tdHeight*2}px`)
          item.style.setProperty('--table-height', `${tdHeight*12}px`)
        })
      })
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
    ...mapActions([
        'addRoom',
        'removeRoom',
        'getSectorsByCameraIDFromDB',
        'getRoomTypesFromDB',
        'getSectorTypesFromDB',
        'getCamerasFromDB'
    ])
  }
}
</script>

<style scoped lang="scss">
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
//.swipe-sector{
//  position: absolute;
//  right: 0;
//  margin-right: 45px;
//  margin-bottom: 5px;
//}
//.show-close-sector{
//  position: absolute;
//  right: 0;
//  margin-right: 20px;
//}
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
  background: linear-gradient(#dfe0ff 50%, #ffffff 50%) local;
  background-size: 100% var(--td-height);
  height: var(--table-height);
  overflow-y: auto;
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
.grid-default{
  display: grid;
  grid-gap: 50px;
  grid-template-columns: 50px 1fr;
}
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
  border-radius: 10px;
}
.sector-name {
  display: inline-block;
  width: 4em;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
//:root{
//  --td-height: 52px;
//  --table-height: 200px;
//}

</style>