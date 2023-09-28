<template>
  <div class="container login">
    <form @submit.prevent="register">
      <div class="form-group">
        <label>Имя: </label>
        <input type="text" v-model.trim="user.name" class="form-control"
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
               :class="v$.user.login.$error ? 'is-invalid' : ''">
        <p v-if="v$.user.login.$dirty && v$.user.login.required.$invalid" class="invalid-feedback">
          Обязательное поле
        </p>
        <p v-if="v$.user.login.$dirty && v$.user.login.minLength.$invalid" class="invalid-feedback">
          Поле должно содержать минимум 3 символа
        </p>
      </div>
      <div class="form-group">
        <label >Пароль: </label>
        <input type="password" v-model.trim="user.password" class="form-control"
               :class="v$.user.password.$error ? 'is-invalid' : ''">
        <p v-if="v$.user.password.$dirty && v$.user.password.required.$invalid" class="invalid-feedback">
          Обязательное поле
        </p>
        <p v-if="v$.user.password.$dirty && v$.user.password.minLength.$invalid" class="invalid-feedback">
          Поле должно содержать минимум 3 символа
        </p>
      </div >
      <div class="row justify-content-around form-group">
        <button type="submit" class="btn btn-success col-auto">Зарегистрироваться</button>
        <button type="button" class="btn btn-primary col-auto"
                @click="this.$emit('registrationCompleted')">
          Назад
        </button>
      </div>
    </form>
  </div>

</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'

export default {
  name: "RegistrationPage",
  setup () {
    return {
      v$: useVuelidate()
    }
  },
  data(){
    return{
      user: {
        name: '',
        surname: '',
        login: '',
        password: '',
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
  methods: {
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
              this.$emit('registrationCompleted')
            });
      }
    }
  }

}
</script>

<style>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 0 20px;
  margin-top: 40px;
}
.form-control {
  width: 400px;
}
.form-group {
  width: 400px;
}
</style>