<template>
  <div class="explorer-parent">
    <div class="explorer window content content-center">
      <form @submit.prevent="selectFunction(updateUser)">
        <div class="form-group">
          <label>Имя: </label>
          <input type="text"  v-model.trim="user.name" class="form-control"
                 :class="v$.user.name.$error ? 'is-invalid' : ''">
          <p v-if="v$.user.name.$dirty && v$.user.name.required.$invalid" class="invalid-feedback">
            Обязательное поле
          </p>
        </div>
        <div class="form-group">
          <label>Фамилия: </label>
          <input type="text" v-model.trim="user.surname" class="form-control"
                 :class="v$.user.surname.$error ? 'is-invalid' : ''">
          <p v-if="v$.user.surname.$dirty && v$.user.surname.required.$invalid" class="invalid-feedback">
            Обязательное поле
          </p>
        </div>
        <div class="form-group">
          <label>Логин: </label>
          <input type="text" v-model.trim="user.login" class="form-control"
                 :class="v$.user.login.$error ? 'is-invalid' : ''" disabled>
          <p v-if="v$.user.login.$dirty && v$.user.login.required.$invalid" class="invalid-feedback">
            Обязательное поле
          </p>
          <p v-if="v$.user.login.$dirty && v$.user.login.minLength.$invalid" class="invalid-feedback">
            Поле должно содержать минимум 3 символа
          </p>
        </div>
        <div class="form-group">
          <label >Пароль: </label>
          <input type="password" autocomplete="new-password" v-model.trim="user.password" class="form-control"
                 :class="v$.user.password.$error ? 'is-invalid' : ''">
          <p v-if="v$.user.password.$dirty && v$.user.password.required.$invalid" class="invalid-feedback">
            Обязательное поле
          </p>
          <p v-if="v$.user.password.$dirty && v$.user.password.minLength.$invalid" class="invalid-feedback">
            Поле должно содержать минимум 3 символа
          </p>
        </div >
        <div class="row justify-content-around form-group">
          <button type="submit" class="btn btn-success col-auto">Подтвердить</button>
          <button type="button" class="btn btn-primary col-auto" @click="$emit('changePassword')">
            Назад
          </button>
        </div>
<!--        <button @click="register">register</button>-->
      </form>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'
import {mapGetters} from "vuex";

export default {
  props:['selectFunction'],
  name: "RegistrationPage",
  setup () {
    return {
      v$: useVuelidate()
    }
  },
  data(){
    return{
      user: {
        id: null,
        name: '',
        surname: '',
        login: '',
        password: ''
      }
    }
  },
  validations: {
    user: {
      name: {required},
      surname: {required},
      login: { required, minLength: minLength(3) },
      password: {required, minLength: minLength(3)},
    }
  },
  computed: {
    ...mapGetters([
        'getUser'
    ])
  },
  mounted() {
    this.user = Object.assign({}, this.getUser)
  },
  methods: {
    change() {
      console.log('change')
    },
    async updateUser() {
      let returnResult
      try{
        returnResult = await fetch('http://localhost:5000/setUserData',{
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
          body: JSON.stringify({
            "id": this.user.id,
            "name": this.user.name,
            "surname": this.user.surname,
            "password": this.user.password
          })
        })
            .then((response) => response.json())
            .then((response) => {
              console.log(response)
              try{
                if (response.setUserData === true) return response
                else{
                  alert('Что-то пошло не так, попробуйте еще раз')
                  console.log()
                }
              } catch (err) {
                console.log(err)
              }
            })
      } catch (err) {
        console.log(err)
      }
      this.$emit('onLogout')
      return returnResult
    },
    setUser() {
      this.v$.user.$touch()
      if (!this.v$.user.$error) {
        fetch('http://localhost:5000/setUserData', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
          },
          body: JSON.stringify({
            "id": this.user.id,
            "name": this.user.name,
            "surname": this.user.surname,
            "password": this.user.password
          })
        })
            .then((response) => {
              console.log(response.json())
            });
      }
    },
    register() {
      this.v$.user.$touch()
      if (!this.v$.user.$error) {
        fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
          },
          body: JSON.stringify({
            'name': this.user.name,
            "surname": this.user.surname,
            "login": this.user.login,
            "password": this.user.password
          })
        })
            .then((response) => {
              console.log(response.json())
            });
      }
    }
  }

}
</script>

<style lang="scss">
//.login {
//  max-width: 400px;
//  /*margin: 0 auto;*/
//  padding: 0 20px;
//  /*margin-top: 40px;*/
//}
.form-control {
  width: 400px;
}
.form-group {
  width: 400px;
}
//.explorer-parent {
//  width: 100%;
//  height: 100%;
//  position: absolute;
//  left: 0;
//  top: 0;
//  display: flex;
//  //align-items: center;
//  //align-content: center;
//  //justify-content: center;
//  z-index: 100;
//  background-color: #ffffff;
//}
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
.explorer{
  width: 450px;
  height: 450px;
  background-color: #ffffff;
}
.explorer-parent {
  width: 100%;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  align-items: center;
  //align-content: center;
  justify-content: center;
  z-index: 100;
  background-color: rgba(218, 218, 218, 0.7);
}
.window{
  box-shadow: 0 3px 4px rgba(0,0,0,.25);
  border-radius: 10px ;
}
</style>