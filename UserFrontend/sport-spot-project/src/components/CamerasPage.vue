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
          <form @submit.prevent="save" style="margin-top: 10px">
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
            <div style="width: 50px; margin-bottom: 10px">
                <button type="submit" class="btn btn-success" >Сохранить</button>
              </div>
          </form>
          <button
              class="btn btn-primary"
              @click="removeCamera(camera.id); resetCamera()"
              style="position: absolute; top: 0; right: 0; margin-right: 15px; margin-top: 308px">
            Удалить
          </button>
          <label style="font-weight: 700">Сектора</label>

          <button style="position: absolute; right: 0; margin-right: 30px" @click="addSectorToCamera">Добавить</button>
          <div v-if="getSectors.length === 0" id="preloaded" class="hidden"></div>
          <div class="" v-for="(cameraSector, index) in getSectorsByCameraID(this.camera.id)" :key="index">
            <input class="input-field-sector" type="text" v-model.trim="cameraSector.name" placeholder="Название">
            <select v-model="cameraSector.typeId">
              <option v-for="(sectorType, index) in getSectorTypes" :value="sectorType.id" :key="index">
                {{sectorType.name}}
              </option>
            </select>
            <button class="hidden-button" @click="chooseSector(cameraSector)" style="margin-left: 5px">
              <img v-if="sectorSelected && sector.id === cameraSector.id" style="margin-bottom: 5px" :src="require('../assets/icons/eye-opened.png')" alt="">
              <img v-else style="margin-bottom: 5px" :src="require('../assets/icons/eye-closed.png')" alt="">
            </button>
            <button class="hidden-button" @click="removeSector(cameraSector.id); drawClear()" style="margin-left: 10px">
              <img style="margin-bottom: 5px" :src="require('../assets/icons/delete.png')" alt="">
            </button>
          </div>
          <br>
        </div>
        <div class="col-5">
          <div class="col-12 window">
            <p>Изображение</p>
            <div style="width: 300px; height: 300px">
<!--              :src="require('')"-->
<!--              <img id="putImage" :src="require('../' + imgPath)"  style="width: 100%; height: 100%"  alt="img1">-->
              <img v-if="cameraSelected" :src="imgPath" style="width: 100%; height: 100%" alt="">
              <img v-else :src="require('@/assets/images/background.png')" alt="">
              <canvas
                  @click="drawLine($event.clientX, $event.clientY)"
                  id="canvas"
                  width="300" height="300"
                  style="position: absolute; top: 0; left: 0; margin-top: 40px; margin-left: 14px"
              >
              </canvas>
            </div>

            <br>
            <button @click="endDraw">Заполнить область</button>
            <button @click="removeSectorPoints">Очистить всё</button>
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
import { required, integer} from '@vuelidate/validators'

export default {
  name: "CamerasPage",
  setup () {
    return {
      v$: useVuelidate()
    }
  },
  data(){
    return {
      ctx: null,
      drawClicks: 0,
      imgPath: '',
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
    }
  },
  computed: {
    ...mapGetters([
        'getCameras',
        'getCameraByID',
        'getSectorTypes',
        'getSectorsByCameraID',
        'getSectors',
        'getSectorByID',
        'getSectorTypeByID'
    ])
  },
  mounted() {
    if (this.getCameras.length === 0){
      this.getCamerasFromDB()
    }
    if (this.getSectorTypes.length === 0){
      this.getSectorTypesFromDB()
    }
    this.draw()
  },
  methods: {
    getSectorTypesFromDB() {
      fetch(`http://localhost:5000/getSectorTypes`, {
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
          });
    },
    getSectorsByCameraIDFromDB() {
      fetch(`http://localhost:5000/getSectorsByCameraID?id=${this.camera.id}`, {
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log('preload')
            // let preloaderEl = document.getElementById('preloaded')
            // preloaderEl.classList.add('hidden');
            console.log('sectors ')
            console.log(response[0])
            this.$store.state.sectors = response
            console.log(this.$store.state.sectors)
          });
    },
    getCamerasFromDB() {
      fetch('http://localhost:5000/getCameras', {
        // fetch('http://localhost:5000/testJWT', {
        method: 'GET',
        // credentials: "include",
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          // 'Access-Control-Allow-Origin': 'http://192.168.169.32:5000',
          // 'Access-Control-Allow-Credentials': 'true',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
            this.$store.state.cameras = response
          });
    },
    setSector(sector){
      console.log('sector ' + sector)
      let returnedSector = fetch('http://localhost:5000/setSector', {
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
            console.log(response)
            sector.id = response.id
            return sector
          })
      return returnedSector
    },
    setCamera() {
      fetch('http://localhost:5000/setCamera', {
        method: 'POST',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify({
          "chanel": this.camera.chanel,
          "codec": this.camera.codec,
          "id": this.camera.id,
          "ip": this.camera.ip,
          "port": this.camera.port, //change
          "login": this.camera.login,
          "name": this.camera.name,
          "password": this.camera.password,
          "fullRoute": this.camera.fullRoute
        })
      })
          .then(response => response.json())
          .then((response) => {
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
                this.setSector(sector)
            })
          });
    },
    save() {
      this.v$.camera.$touch()
      if (!this.v$.camera.$error) {
        console.log('Валидация прошла успешно')
        this.setCamera()
      }
      else console.log('Валидация не прошла')
    },
    endDraw() {
      this.ctx.lineTo(this.sector.points[0][0], this.sector.points[0][1])
      this.ctx.stroke()
      this.ctx.fillStyle = "rgba(255, 230, 0, 0.25)"
      this.ctx.fill()
      this.drawClicks = 0
    },
    drawLine(x, y){
      if (this.sectorSelected){
        let targetCoords = document.getElementById('canvas').getBoundingClientRect()
        let newX = x - targetCoords.left
        let newY = y - targetCoords.top
        console.log(`x: ${x} y: ${y} newX: ${newX} newY: ${newY} left: ${targetCoords.left} right: ${targetCoords.top}`)
        if (this.drawClicks === 0) {
          this.ctx.moveTo(newX, newY)
        }
        else this.ctx.lineTo(newX, newY)
        this.sector.points.push([newX, newY])
        this.ctx.arc(newX, newY, 2, 0, Math.PI * 2)
        this.ctx.strokeStyle = "rgba(255, 230, 0)"
        this.ctx.lineWidth = 2
        this.ctx.stroke()
        this.drawClicks ++
      }
      else alert("Выберите сектор")
    },
    draw() {
      let canvas = document.getElementById('canvas')
      if (canvas.getContext) {
        console.log('getContext')
        this.ctx = canvas.getContext("2d")
        this.ctx.beginPath()
      }
    },
    removeSectorPoints(){
      this.ctx.clearRect(0, 0, 300, 300)
      this.sector.points = []
      this.ctx.beginPath()
    },
    drawClear() {
      this.ctx.clearRect(0, 0, 300, 300)
      this.ctx.beginPath()
    },
    drawSectorPoints() {
      console.log('drawSectorPoints')
      let points = this.sector.points
      this.ctx.moveTo(points[0][0], points[0][1])
      this.ctx.arc(points[0][0], points[0][1], 2, 0, Math.PI * 2)
      for (let i = 1; i < points.length; i++){
        this.ctx.lineTo(points[i][0], points[i][1])
        this.ctx.arc(points[i][0], points[i][1], 2, 0, Math.PI * 2)
      }
      this.ctx.lineTo(points[0][0], points[0][1])
      this.ctx.strokeStyle = "rgba(255, 230, 0)"
      this.ctx.fillStyle = "rgba(255, 230, 0, 0.25)"
      this.ctx.lineWidth = 2
      this.ctx.stroke()
      this.ctx.fill()
      //
    },
    drawImage() {
      console.log('drawImage')
      this.imgPath='http://localhost:5000/getVideo?camId=' + this.camera.id
      let refreshInterval = setInterval(() => this.refreshCamera(refreshInterval), 5000)

      // img
      // console.log(img)
      // this.ctx.drawImage(img, 0, 0, 779, 584, 0, 0, 300, 300)
    },
    refreshCamera(refreshInterval){
        console.log('check ' + this.cameraSelected)
        if (this.cameraSelected === false){
          console.log('!cameraSelected')
          clearInterval(refreshInterval)
        }
        else{
          console.log('refresh')
          this.refreshVideo()
        }
    },
    refreshVideo() {
      fetch(`http://localhost:5000/refreshVideo?camId=${this.camera.id}`, {
        method: 'GET',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
        },
      })
          .then(response => response.json())
          .then((response) => {
            console.log(response)
          });
    },
    chooseCamera(camera) {
      console.log(camera.id)
      this.camera = this.getCameraByID(camera.id)
      this.getSectorsByCameraIDFromDB()
      this.cameraSelected = true
      this.drawImage()
      this.resetSector()
    },
    chooseSector(sector) {
      if (this.sector.id === sector.id && sector.id !== null) {
        console.log(this.sector.id + ' ' + sector.id + ' resetSec')
        this.resetSector()
      }
      else if (sector.name === '' || sector.typeId === null) alert("Сначала введите название сектора и выберите его тип")
      else if (sector.id === null) {
        let p1 = this.setSector(sector)
        p1.then(value => {
          console.log(value.id)
          this.showSector(value)
        })
      }
      else this.showSector(sector)
    },
    showSector(sector) {
      if (sector.id !== null) {
        this.sector = this.getSectorByID(sector.id)
        this.sectorSelected = true
        this.drawClear()
        if (this.sector.points.length !== 0) {
          this.drawSectorPoints()
        }
      }
    },
    resetCamera(){
      console.log('reset')
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
      this.cameraSelected = false
      this.v$.camera.$reset()
      this.resetSector()
      this.drawClear()
    },
    resetSector() {
      this.drawClear()
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
        'removeSector'
    ])
  }
}
</script>

<style scoped>
canvas {
  border: 1px solid black;
  background: none;
}
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
  width: 25px;
  /*vertical-align: center;*/
}
.hidden-button:hover{
  background-color: #dadada;
  cursor: pointer;
}
</style>