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
        <div class="col-3 scroll scroll-rooms" >
          <div  :style="room.id === selectedRoom.id ? {background: '#a7a7a7'} : '' "
                class="row window camera col-12"
                @click="chooseRoom(selectedRoom)"
                v-for="(selectedRoom, index) in getRooms"
               :key="index">
            <span class="room-name short-name short-name-room" :title="selectedRoom.name">{{selectedRoom.name}}</span>
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
            <div id="buttons" class="grid-default" style="margin-bottom: 10px">
              <button type="submit" class="btn btn-success" >Сохранить</button>
              <button
                  type="button"
                  class="btn btn-primary"
                  @click="selectFunction(removeRoom, room.id); resetRoom()">
                Удалить
              </button>
            </div>
          </form>

          <label style="font-weight: 700">Сектора</label>
          <div class="row" v-if="roomSelected">
            <div class="col-6">
              <label>Назначенные</label>
              <div id="table-used" class="window linear-table scroll">
                <table >
                  <tr  v-for="(camera, index) in getUsedCameras" :key="index">
                    <td style="width: 200px" >
                      <div style="height: 26px">
                      <span
                          style="margin-left: 5px"
                          class="short-name short-name-camera"
                          :title="camera.name">
                        {{ camera.name }}
                      </span>
                      </div>
                      <table>
                        <tr v-for="(cameraSector, index) in camera.sectors" :key="index" >
                          <td style="padding: 0">
                            <div id="td-height-used" class="grid-default grid-default-sector" style="height: 26px">
                              <div style="margin-left: 20px">
                                <span class="short-name short-name-sector" :title="cameraSector.name">{{ cameraSector.name }}</span>
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
              <div id="table-unused" class="window linear-table scroll">
                <table >
                  <tr v-for="(camera, index) in getUnusedCameras" :key="index">
                    <td style="width: 200px" >
                      <div style="height: 26px">
                      <span
                          style="margin-left: 5px"
                          class="short-name short-name-camera"
                          :title="camera.name">
                        {{ camera.name }}
                      </span>
                      </div>
                      <table>
                        <tr v-for="(cameraSector, index) in camera.sectors" :key="index" >
                          <td style="padding: 0">
                            <div id="td-height-unused" class="grid-default grid-default-sector" style="height: 26px">
                              <div :style="cameraSector.typeId === 1 && cameraSector.points.length === 0 ? '' : 'margin-left: 20px'">
                                <div class="grid-default">
                                  <div style="display: flex; flex-wrap: wrap; align-content: center; margin-left: 5px">
                                    <img
                                        v-if="cameraSector.typeId === 1 && cameraSector.points.length === 0"
                                        :src="require('../assets/icons/danger16.png')"
                                        alt=""
                                        title="У сектора данного типа отсутствует область анализа">
                                  </div>
                                  <span class="short-name short-name-sector" :title="cameraSector.name">{{ cameraSector.name }}</span>
                                </div>
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
  emits: ['onLogout'],
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
        this.setRoom().then((response) => {
          if (!this.roomSelected){
            this.resetRoom().then(() => {
              console.log('setAfterReset')
              this.chooseRoom(this.getRoomByID(response.id))
            })
          }
        })
      }
      else console.log('Валидация не прошла')
      return returnResult
    },
    async setRoom() {
      let returnResult
      try{
        returnResult = await fetch('http://localhost:5000/setRoom', {
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
              if (response.id) {
                this.room.id = response.id
                if (this.getRoomByID(response.id) === undefined) {
                  this.addRoom(Object.assign({}, this.room))
                  console.log('yesCheck')
                }
              }
              return response
            })
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
    async getUnusedCameraSectorsByRoomIdFromDB() {
      let returnResult
      try{
        console.log('getUnused')
        returnResult = await fetch(`http://localhost:5000/getUnusedCameraSectorsByRoomId?roomId=${this.room.id}`, {
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
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
    async getUsedCameraSectorsByRoomIdFromDB() {
      let returnResult
      try{
        returnResult = await fetch(`http://localhost:5000/getCameraSectorsByRoomId?roomId=${this.room.id}`, {
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
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
    async getRoomsFromDB() {
      let returnResult
      try{
        returnResult = await fetch('http://localhost:5000/getRooms', {
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
      } catch (err) {
        console.log(err)
      }
      return returnResult
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
              this.$refs.showCamera.convertToPixels()
            }
            clearInterval(interval)
          }
        }, 100)
      }
    },
    async resetRoom(){
      new Promise((resolve) => {
        let roomCopy = Object.assign({}, this.room)
        this.room = roomCopy
        this.room.name = ''
        this.room.classId = null
        this.room.id = null
        this.room.sportObjectId = ''
        this.$store.state.unusedCameras = {}
        this.$store.state.usedCameras = {}
        this.v$.room.$reset()
        this.roomSelected = false
        this.resetSector()
        resolve('ok')
      })
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
      console.log('reload')
      this.selectFunction(this.getUsedCameraSectorsByRoomIdFromDB)
      this.selectFunction(this.getUnusedCameraSectorsByRoomIdFromDB).then(() => {
        let tdHeight = 26
        // try{
        //   tdHeight = document.getElementById("td-height-unused").offsetHeight
        // } catch (err) {
        //   tdHeight = document.getElementById("td-height-used").offsetHeight
        // }
        let linearTable = document.getElementsByClassName('linear-table')
        Array.from(linearTable).forEach((item) => {
            item.style.setProperty('--td-height', `${tdHeight*2}px`)
          item.style.setProperty('--table-height', `${tdHeight*12}px`)
        })
      })
    },
    async setSectorToRoom(sector){
      let returnResult
      try{
        returnResult = await fetch(`http://localhost:5000/setSectorToRoom?sectorId=${sector.id}&roomId=${this.room.id}`, {
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
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
    async removeSectorFromRoom(sector){
      let returnResult
      try{
        returnResult = await fetch(`http://localhost:5000/removeSectorFromRoomLsit?sectorId=${sector.id}&roomId=${this.room.id}`, {
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
      } catch (err) {
        console.log(err)
      }
      return returnResult
    },
    ...mapActions([
        'addRoom',
        'removeRoom',
        'getSectorsByCameraIDFromDB',
        'getRoomTypesFromDB',
        'getSectorTypesFromDB',
        'getCamerasFromDB',
        'setSectorToDB'
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
}
.scroll{
  overflow-y: auto;
  &-rooms{
    height: 550px;
  }
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
  grid-gap: 10px;
  grid-template-columns: 1fr 1fr;
  &-sector{
    grid-gap: 30px;
    grid-template-columns: 70px 1fr;
  }
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
//.sector-name {
//  display: inline-block;
//  width: 4em;
//  overflow: hidden;
//  white-space: nowrap;
//  text-overflow: ellipsis;
//}
.short-name {
  display: inline-block;
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  &-room{
    width: 80%;
  }
  &-camera{
    width: 8em;
  }
  &-sector{
    width: 4em;
  }
}
td{
  padding: 0;
}
//:root{
//  --td-height: 52px;
//  --table-height: 200px;
//}

</style>