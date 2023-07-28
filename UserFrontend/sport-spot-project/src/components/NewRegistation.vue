<template>

<div class="container login">

    <form @submit.prevent="checkForm">
        <div class="form-group">
            <label for="login">Login: </label>
            <input type="text" v-model.trim="user.login" class="form-control"
             :class="v$.user.login.$error ? 'is-invalid' : ''">
             <p v-if="v$.user.login.$dirty && v$.user.login.required.$invalid" class="invalid-feedback">
                Обязательное поле
            </p>
             <p v-if="v$.user.login.$dirty && v$.user.login.minLength.$invalid" class="invalid-feedback">
                Поле должно содержать минимум 5 символов
            </p>
        </div>

        <div class="form-group">
            <label for="password">Password: </label>
            <input type="password" v-model.trim="user.password" class="form-control"
            :class="v$.user.password.$error ? 'is-invalid' : ''">
            <p v-if="v$.user.password.$dirty && v$.user.password.required.$invalid" class="invalid-feedback">
                Обязательное поле
            </p>
             <p v-if="v$.user.password.$dirty && v$.user.password.minLength.$invalid" class="invalid-feedback">
                Поле должно содержать минимум 5 символов
            </p>

        </div >
        <div class="row justify-content-around form-group">
            <button type="submit" class="btn btn-primary col-auto" >Войти</button>
            <button class="btn btn-success col-auto" @click="request">Отправить запрос</button>
        </div>
        
    </form>
</div>
    
</template>

<script>
import { useVuelidate } from '@vuelidate/core'

import { required, minLength } from '@vuelidate/validators'

    export default{
        props: ['onLogin'],
        name: "NewRegistration",
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
                autorized: false


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

               this.v$.user.$touch()
                if (!this.v$.user.$error) {
                    console.log('Валидация прошла успешно')
                    this.autorized = true
                    this.$emit('sendLogin', this.autorized)
                }
                else console.log('Валидация не прошла')
            },

            created() {
                console.log('post request')

                    fetch('http://192.168.43.243:5000/authorize', {
                          method: 'POST',
                          headers: {
                            'Content-Type': 'application/json;charset=utf-8'
                          },
                          body: JSON.stringify({'login': this.user.login, "password": this.user.password})
                        })
                        .then(response => this.accessToken = response.text())
                        .then((response) => {
                            console.log(response)
                        });
                        console.log(this.accessToken)
            },
            request() {
                fetch('http://192.168.43.243:5000/getTestData', {
                          method: 'POST',
                          headers: {
                            'Authentication': 'Bearer {' + this.accessToken +'}',
                            'Content-Type': 'application/json;charset=utf-8'
                          }
                        })
                        .then(response => response.text())
                        .then((response) => {
                            console.log(response)
                        });

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