<template>
  <div>
    <div class="container" >
      <div class="row justify-content-around">
        <div class="col-2" >
          <div class="row camera" v-for="(camera, index) in getCameras"
               :key="index">
            <label >{{camera.name}}</label>
          </div>
        </div>
        <div class="col-4 form-group">
          <form @submit.prevent="saveCamera">
            <div class="form-group">
              <label> Название: </label>
              <input class="form-control" type="text" v-model.trim="camera.name"
                     :class="v$.camera.name.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.name.$dirty && v$.camera.name.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group">
              <label> IP: </label>
              <input class="form-control" type="text" v-model.trim="camera.IP"
                     :class="v$.camera.IP.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.IP.$dirty && v$.camera.IP.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group">
              <label> Канал: </label>
              <input class="form-control" type="text" v-model.trim="camera.channel"
                     :class="v$.camera.channel.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.channel.$dirty && v$.camera.channel.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group">
              <label> Кодек: </label>
              <input class="form-control" type="text" v-model.trim="camera.codec"
                     :class="v$.camera.codec.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.codec.$dirty && v$.camera.codec.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group">
              <label> Логин: </label>
              <input class="form-control" type="text" v-model.trim="camera.login"
                     :class="v$.camera.login.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.login.$dirty && v$.camera.login.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="form-group">
              <label> Пароль: </label>
              <input class="form-control" type="text" v-model.trim="camera.password"
                     :class="v$.camera.password.$error ? 'is-invalid' : ''">
              <p v-if="v$.camera.password.$dirty && v$.camera.password.required.$invalid" class="invalid-feedback">
                Обязательное поле
              </p>
            </div>
            <div class="row form-group">
              <button type="submit" class="btn btn-primary" >Сохранить камеру</button>
            </div>
          </form>
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
  name: "CamerasPage",
  setup () {
    return {
      v$: useVuelidate()
    }
  },
  data(){
    return {
      camera: {
        name: '',
        IP: '',
        channel : '',
        codec : '',
        login : '',
        password : ''
      }
    }
  },
  validations: {
    camera: {
      name: {required},
      IP: {required},
      channel: {required},
      codec: {required},
      login: { required },
      password: {required},
    }
  },
  computed: {
    ...mapGetters([
        'getCameras'
    ]),
  },
  methods: {
    saveCamera() {
      this.v$.camera.$touch()
      if (!this.v$.camera.$error) {
        console.log('Валидация прошла успешно')
        this.addCamera(this.camera)
      }
      else console.log('Валидация не прошла')
    },
    ...mapActions([
      'addCamera'
    ])
  }
}
</script>

<style scoped>
.camera{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
}
</style>