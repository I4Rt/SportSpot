<template>
<div class="container login">
      <form @submit.prevent="created">
        <div class="">
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
            <button type="submit" class="btn btn-success col-auto">Войти</button>
<!--          <button type="button" class="btn btn-primary col-auto"-->
<!--                  @click="this.$emit('registerUser')">-->
<!--            Зарегистрироваться-->
<!--          </button>-->
        </div>
    </form>

</div>
    
</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'

    export default{
        props: ['onLogin'],
        name: "AuthorizationPage",
        setup () {
            return {
                v$: useVuelidate()
            }
        },
        data(){
            return {
                user: {
                    login: '',
                    password: '',
                },
                accessToken: '',
                authorized: false,
                accessLogin: false,

            }
        },
        validations: {
            user: {
                login: { required, minLength: minLength(3) },
                password: {required, minLength: minLength(3)},
            }
        },
        methods: {
            checkForm() {
                  if (this.accessLogin === true){
                    console.log('check')
                    this.authorized = true
                    this.$emit('sendLogin', this.authorized)
                  }
            },
            created() {
              this.v$.user.$touch()
              if (!this.v$.user.$error) {
                console.log('post request')
                fetch('http://localhost:5000/authorize', {
                  method: 'POST',
                  credentials: "include",
                  cors: 'no-cors',
                  headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                  },
                  body: JSON.stringify({'login': this.user.login, "password": this.user.password})
                })
                    .then(response => response.json())
                    .then((response) => {
                      console.log(response)
                      if (response.login === true) {
                        this.accessLogin = true
                        this.checkForm()
                      }
                      else if (response.login === false) {
                        alert('Неверный логин или пароль')
                      }
                    });
              }
              else console.log('Валидация не прошла')
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
.btn-login {
    width: 200px;
    align-content: center;
}

</style>