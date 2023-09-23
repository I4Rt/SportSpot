<template>
  <div>
    <div class="container" >
      <div class="row justify-content-around">
        <div class="col-3">
            <div class="row">
              <label class="field">Камеры</label>
              <button class="add" style="margin-top: 5px" @click="resetCamera">Добавить</button>
            </div>
        </div>
        <div class="col-4">
          <label class="field">Настройка</label>
        </div>
        <div class="col-5">
          <label class="field">Просмотр</label>
        </div>
        <div class="col-3" >
          <div class="row window camera col-12" @click="chooseCamera(camera)" v-for="(camera, index) in getCameras"
               :key="index">
              <span class="cam-name">{{camera.name}}</span>
              <span class="cam-ip">{{camera.ip}}</span>
          </div>
        </div>
        <div class="col-4 window">
          <label style="font-weight: 700; margin-top: 10px">Изображение</label>
          <form style="margin-top: 10px" @submit.prevent="save" class="needs-validation">
            <div class="">
              <label> Название: </label>
              <input class=" input-field" type="text" v-model.trim="camera.name"
                     :class="v$.camera.name.$error ? 'is-invalid' : ''" >
              <p v-if="v$.camera.name.$dirty && v$.camera.name.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> ip: </label>
              <input class="input-field" type="text" v-model.trim="camera.ip"
                     :class="v$.camera.ip.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.ip.$dirty && v$.camera.ip.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> Порт: </label>
              <input class="input-field" type="text" v-model.trim="camera.port"
                     :class="v$.camera.port.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.port.$dirty && v$.camera.port.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
              <p v-if="v$.camera.port.$dirty && v$.camera.port.integer.$invalid " class="invalid-feedback">
                Значение должно быть числовым
              </p>
            </div>
            <div class="">
              <label> Канал: </label>
              <input class="input-field" type="text" v-model.trim="camera.chanel"
                     :class="v$.camera.chanel.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.chanel.$dirty && v$.camera.chanel.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
              <p v-if="v$.camera.chanel.$dirty && v$.camera.chanel.integer.$invalid " class="invalid-feedback">
                Значение должно быть числовым
              </p>
            </div>
            <div class="">
              <label> Кодек: </label>
              <input class="input-field" type="text" v-model.trim="camera.codec"
                     :class="v$.camera.codec.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.codec.$dirty && v$.camera.codec.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> Логин: </label>
              <input class="input-field" type="text" v-model.trim="camera.login"
                     :class="v$.camera.login.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.login.$dirty && v$.camera.login.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> Пароль: </label>
              <input class="input-field" type="text" v-model.trim="camera.password"
                     :class="v$.camera.password.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.password.$dirty && v$.camera.password.required.$invalid " class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> Полный путь: </label>
              <input class="input-field" type="text" v-model.trim="camera.fullRoute">
            </div>
            <div id="buttons" class="grid-default" style="margin-bottom: 10px">
              <button type="submit" class="btn btn-success" >Сохранить</button>
              <button
                  type="button"
                  class="btn btn-primary"
                  @click="removeCamera(camera.id); resetCamera()">
                Удалить
              </button>
            </div>
          </form>

          <label style="font-weight: 700">Секторы</label>

          <button style="position: absolute; right: 0; margin-right: 30px" @click="addSectorToCamera">Добавить</button>
          <div v-if="getSectors.length === 0" id="preloaded" class="hidden"></div>
          <div v-for="(cameraSector, index) in getSectorsByCameraID(this.camera.id)" :key="index">
            <div class="grid-default sectors">
                <input class="input-field-sector" type="text" v-model.trim="cameraSector.name" placeholder="Название">
                <select v-model="cameraSector.typeId">
                  <option v-for="(sectorType, index) in getSectorTypes" :value="sectorType.id" :key="index">
                    {{sectorType.name}}
                  </option>
                </select>
                <button class="hidden-button content content-center" @click="chooseSector(cameraSector)">
                  <img v-if="sectorSelected && sector.id === cameraSector.id" style="margin-bottom: 5px" :src="require('../assets/icons/eye-opened.png')" alt="">
                  <img v-else style="margin-bottom: 5px" :src="require('../assets/icons/eye-closed.png')" alt="">
                </button>
                <button
                    class="hidden-button"
                    @click="selectFunction(removeSector,cameraSector.id); $refs.showCamera.drawClear()">
                  <img style="margin-bottom: 5px" :src="require('../assets/icons/delete.png')" alt="">
                </button>
            </div>
          </div>
          <br>
        </div>
        <div class="col-5">
          <show-camera
          :cameraID="camera.id"
          :sector="sector"
          :selectFunction="selectFunction"
          :sectorSelected=sectorSelected
          :cameraSelected="cameraSelected"
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
import { required, integer} from '@vuelidate/validators'
import ShowCamera from "@/components/ShowCamera";

export default {
  props: ['selectFunction'],
  name: "CamerasPage",
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
      drawClicks: 0,
      camera: {
        id : null,
        roomID: null,
        name: '',
        ip: '',
        port: '',
        chanel : '',
        codec : '',
        login : '',
        password : '',
        fullRoute: '',
      },
      sector: {
        camId: null,
        id: null,
        name: '',
        points: [],
        roomId: null,
        typeId: null,
      },
      cameraSelected: false,
      sectorSelected: false
    }
  },
  validations: {
    camera: {
      name: {required},
      ip: {required},
      port: {required, integer},
      chanel: {required, integer},
      codec: {required},
      login: { required },
      password: {required},
    },
  },
  computed: {
    ...mapGetters([
        'getCameras',
        'getCameraByID',
        'getSectorTypes',
        'getSectorsByCameraID',
        'getSectors',
        'getSectorByID',
        'getSectorTypeByID',
        'getRefreshInterval'
    ])
  },
  mounted() {
    console.log('mountedCameras')
    this.selectFunction(this.getCamerasFromDB)
    if (this.getSectorTypes.length === 0){
      this.selectFunction(this.getSectorTypesFromDB)
    }
  },
  methods: {
    async getSectorTypesFromDB() {
      let returnResult
      fetch(`http://localhost:5000/getSectorTypes`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            returnResult = response
            console.log('sectorTypes ')
            this.$store.state.sectorTypes = response
            console.log(this.$store.state.sectorTypes)
          });
      return returnResult
    },
    getSectorsByCameraIDFromDB() {
      let returnResult
      fetch(`http://localhost:5000/getSectorsByCameraID?id=${this.camera.id}`, {
        credentials: "include",
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            returnResult = response
            // console.log('preload')
            // let preloaderEl = document.getElementById('preloaded')
            // preloaderEl.classList.add('hidden');
            console.log('sectors ')
            console.log(response[0])
            this.$store.state.sectors = response
            console.log(this.$store.state.sectors)
          });
      return returnResult
    },
    // getCamerasFromDB() {
    //   let returnResult
    //   fetch('http://localhost:5000/getCameras', {
    //     credentials: "include",
    //     method: 'GET',
    //     cors: 'no-cors',
    //     headers: {
    //       'Content-Type': 'application/json;charset=utf-8',
    //     },
    //   })
    //       .then(response => response.json())
    //       .then((response) => {
    //         returnResult = response
    //         console.log(response)
    //         this.$store.state.cameras = response
    //       });
    //   return  returnResult
    // },
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
    async setCamera() {
      return fetch('http://localhost:5000/setCamera', {
        credentials: "include",
        method: 'POST',
        // cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify({
          "chanel": this.camera.chanel,
          "codec": this.camera.codec,
          "id": this.camera.id,
          "ip": this.camera.ip,
          "port": this.camera.port,
          "login": this.camera.login,
          "name": this.camera.name,
          "password": this.camera.password,
          "fullRoute": this.camera.fullRoute
        })
      })
          .then(response => response.json())
          .then((response) => {
            console.log('setCameraResponse ' + response)
            console.log(response)

            this.camera.id = response.id
            let cameraCopy = Object.assign({}, this.camera)
            console.log('check')
            if (this.getCameraByID(cameraCopy.id) === undefined) {
              this.addCamera(cameraCopy)
              console.log('yesCheck')
            }
            console.log('noCheck')
            this.getSectors.forEach((sector) => {
              sector.camId = this.camera.id
              this.selectFunction(this.setSector, sector)
            })
            return response
          });
    },
    save() {
      this.v$.camera.$touch()
      console.log('save')
      if (!this.v$.camera.$error) {
        console.log('Валидация прошла успешно')
        this.selectFunction(this.setCamera)
      }
      else console.log('Валидация не прошла')
    },
    chooseCamera(camera) {
      this.resetCamera()
      console.log(camera.id)
      this.camera = this.getCameraByID(camera.id)
      this.cameraSelected = true
      console.log(this.camera.id)
      this.selectFunction(this.getSectorsByCameraIDFromDB)

      //ожидание корректного ID камеры
      let interval = setInterval(() => {
        console.log('id' + camera.id + ' ' + this.camera.id)
        if (this.camera.id === camera.id){
          this.$refs.showCamera.drawImage()
          clearInterval(interval)
        }
      }, 100)
      this.resetSector()
    },
    chooseSector(cameraSector) {
      if (this.sector.id === cameraSector.id && cameraSector.id !== null) {
        console.log(this.sector.id + ' ' + cameraSector.id + ' resetSec')
        this.resetSector()
      }
      else if (cameraSector.name === '' || cameraSector.typeId === null) alert("Сначала введите название сектора и выберите его тип")
      else if (cameraSector.id === null) {
        let p1 = this.selectFunction(this.setSector, cameraSector)
        p1.then(() => {
          console.log('4 value')
          console.log(cameraSector)
          this.showSector(cameraSector)
        })
      }
      else this.showSector(cameraSector)
    },
    showSector(sector) {
      console.log('5 show')
      if (sector.id !== null) {
        this.sector = this.getSectorByID(sector.id)
        this.sectorSelected = true
        this.$refs.showCamera.drawClear()
        if (this.sector.points.length !== 0) {

          console.log(this.sector)
          this.$refs.showCamera.drawSectorPoints()
        }
      }
    },
    resetCamera(){
      // this.$refs.showCamera.changeImgPath('@/assets/images/background.png')
      console.log('reset')
      this.cameraSelected = false
      this.$store.state.sectors = []
      let cameraCopy = Object.assign({}, this.camera)
      this.camera = cameraCopy
      this.camera.id = null
      this.camera.roomID = null
      this.camera.name = ''
      this.camera.ip = ''
      this.camera.codec = ''
      this.camera.port = ''
      this.camera.chanel = ''
      this.camera.login = ''
      this.camera.password = ''
      this.camera.fullRoute = ''
      this.$refs.showCamera.changeImgPath("data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=")
      this.v$.camera.$reset()
      this.resetSector()
      this.$refs.showCamera.drawClear()

      if (this.getRefreshInterval){
        console.log('clean')
        this.$store.commit('clearRefreshInterval')
      }
    },
    resetSector() {
      this.$refs.showCamera.drawClear()
      let sectorCopy = Object.assign({}, this.sector)
      this.sector = sectorCopy
      this.sector.camId = null
      this.sector.id = null
      this.sector.name = ''
      this.sector.points = []
      this.sector.roomId = null
      this.sector.typeId = null
      this.sectorSelected = false
    },
    addSectorToCamera() {
      console.log('p')
      this.resetSector()
      this.sector.camId = this.camera.id
      this.$store.commit('setSector', Object.assign({}, this.sector))
    },
    ...mapActions([
        'addCamera',
        'removeCamera',
        'removeSector',
        'getCamerasFromDB'
    ])
  }
}
</script>

<style scoped lang="scss">
#preloaded {
  position: inherit;
  left: 0;
  top: 0;
  z-index: 999;
  width: 100%;
  height: 30%;
  overflow: visible;
  background: #fbfbfb url('//cdnjs.cloudflare.com/ajax/libs/file-uploader/3.7.0/processing.gif') no-repeat center center;
}
.hidden{
  visibility: hidden;
  opacity: 0;
}
.visible{
  visibility: visible;
  opacity: 1;
}
.window{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
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
.input-field-sector{
  outline: none;
  width: 150px;
  height: 25px;
  font-size: 14px;
  margin-right: 15px;
  border-radius: 5px ;
  border: 1px solid grey;
}
.camera:hover{
  background-color: #dadada;
  cursor: pointer;
}
.cam-name{
  font-size: 14px;
  font-weight: 500;
  margin: 7px;
}
.cam-ip{
  font-size: 12px;
  font-weight: 300;
  position: absolute;
  right: 0;
  margin-right: 30px;
  margin-top: 10px;
}
.add{
  width: 110px;
  /*height: 35px;*/
  position: absolute;
  right: 0;
  /*top: 0;*/
  margin-right: 30px;
  border-radius: 10px;
  font-size: 18px;
}
.add:hover{
  background-color: #dadada;
}
.field {
  font-size: 22px;
  font-weight: 700;
}
.hidden-button{
  background: inherit;
  border: none;
  //width: auto;
  /*vertical-align: center;*/
}
.hidden-button:hover{
  background-color: #dadada;
  cursor: pointer;
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
}
.sectors{
  grid-template-columns: repeat(4, 1fr)
}
</style>