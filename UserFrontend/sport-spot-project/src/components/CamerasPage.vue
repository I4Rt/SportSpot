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
              <span class="cam-ip">{{camera.IP}}</span>
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
              <label> IP: </label>
              <input class="input-field" type="text" v-model.trim="camera.IP"
                     :class="v$.camera.IP.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.IP.$dirty && v$.camera.IP.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="">
              <label> Канал: </label>
              <input class="input-field" type="text" v-model.trim="camera.channel"
                     :class="v$.camera.channel.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.channel.$dirty && v$.camera.channel.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
              <p v-if="v$.camera.channel.$dirty && v$.camera.channel.integer.$invalid " class="invalid-feedback">
                Канал должен быть числом
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
            <div class="form-group" >
              <button type="submit" class="btn btn-primary" >Сохранить</button>
            </div>
          </form>
          <label style="font-weight: 700">Сектора</label>
          <button style="position: absolute; right: 0; margin-right: 30px" @click="addSectorToCamera">Добавить</button>
          <div class="" v-for="(cameraSector, index) in camera.sectors" :key="index">
            <input class="input-field-sector" type="text" v-model.trim="cameraSector.name" placeholder="Название">
            <select v-model="cameraSector.type">
              <option v-for="(sectorType, index) in getSectorTypes" :key="index">
                {{sectorType}}
              </option>
            </select>
          </div>
          <br>
        </div>
        <div class="col-5">
          <div class="col-12 window">
            <p>Изображение</p>
<!--            <img src="http://192.168.248.32:5000/videoStream" style="width: 100%">-->
            <img :src="require('../assets/images/img1.png')" style="width: 100%" alt="img1">
            <p>Информация сектора</p>
            <p>Сектор</p>
            <span>Техническая информация:</span>
            <ul>
              <li>Границы:</li>
              <li>Высота от пола:</li>
              <li>Тип сектора: <span v-if="cameraSelected">{{camera.sectors.type}}</span></li>
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
      camera: {
        id : -1,
        roomID: -1,
        name: '',
        IP: '',
        channel : '',
        codec : '',
        login : '',
        password : '',
        sectors: []
      },
      sector: {
        id: -1,
        name: '',
        type: ''
      },
      count: 0,
      cameraSelected: false
    }
  },
  validations: {
    camera: {
      name: {required},
      IP: {required},
      channel: {required, integer},
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
        'getCameraCount'
    ]),
  },
  methods: {
    setCamera() {
      fetch('http://192.168.248.32:5000/setCamera', {
        method: 'POST',
        cors: 'no-cors',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',

        },
        body: JSON.stringify({
          "chanel": this.camera.channel,
          "codec": this.camera.codec,
          "id": null,
          "ip": this.camera.IP,
          "login": this.camera.login,
          "name": this.camera.name,
          "password": this.camera.password
        })
      })
          .then(response => response["id"])
          .then((response) => {
            console.log(response)
          });
    },
    save() {
      this.v$.camera.$touch()
      if (!this.v$.camera.$error) {
        console.log('Валидация прошла успешно')
        // this.setCamera()
        this.camera.id = this.getCameraCount
        this.addCameraCount(this.getCameraCount + 1)
        let cameraCopy = Object.assign({}, this.camera)
        let sectorsCopy = Object.assign({}, this.camera.sectors)
        cameraCopy.sectors = sectorsCopy
        this.addCamera(cameraCopy)
        this.v$.camera.$reset()
      }
      else console.log('Валидация не прошла')
    },
    chooseCamera(camera) {
      console.log(camera.id)
      this.camera = this.getCameraByID(camera.id)
      this.cameraSelected = true
    },
    resetCamera(){
      let cameraCopy = Object.assign({}, this.camera)
      // let sectorsCopy = Object.assign({}, this.camera.sectors)
      // cameraCopy.sectors = sectorsCopy
      this.camera = cameraCopy
      this.camera.id = -1
      this.camera.roomID = -1
      this.camera.name = ''
      this.camera.IP = ''
      this.camera.codec = ''
      this.camera.channel = ''
      this.camera.login = ''
      this.camera.password = ''
      this.camera.sectors = []
      this.cameraSelected = false
      this.sector.name = ''
      this.sector.type = ''
      this.sector.id = -1
    },
    addSectorToCamera() {
      this.sector.id = this.count
      this.count++
      this.camera.sectors.push(Object.assign({}, this.sector))
    },
    ...mapActions([
      'addCamera',
        'addCameraCount'
    ])
  }
}
</script>

<style scoped>
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
</style>