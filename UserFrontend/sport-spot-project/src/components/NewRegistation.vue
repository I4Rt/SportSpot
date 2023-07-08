<template>
<div class="container">
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
        <!-- <div class="form-group"> 
            <label for="email">Email: </label>
            <input type="email" v-model.trim="user.email" class="form-control"
            :class="v$.user.email.$error ? 'is-invalid' : ''">
            <p v-if="v$.user.email.$dirty && v$.user.email.required.$invalid" class="invalid-feedback">
                Обязательное поле
            </p>
             <p v-if="v$.user.email.$dirty && v$.user.email.$invalid" class="invalid-feedback">
                В поле должна быть указана почта
            </p>
        </div> -->
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
        </div>
        <!-- <div class="form-group">
            <label for="country">Страна проживания: </label>
            <select v-model="user.country" class="form-control">
                <option v-for="(country, index) in countries" :key="index">
                    {{country}}
                </option>
            </select>
        </div> -->
        <!-- <div class="form-check">
            <input type="checkbox" v-model="user.agreeWithRules" class="form-check-input "
            :class="v$.user.agreeWithRules.$error ? 'is-invalid' : ''">
            <label class="form-check-label">Ознакомлен с пользовательским соглашением </label>
            <p v-if="v$.user.agreeWithRules.$dirty && !v$.user.agreeWithRules.mustBeTrue.$response" class="invalid-feedback">
                Обязательное поле
            </p>
        </div> -->
        <button type="submit" class="btn btn-login btn-primary" @click="created">Войти</button>
        <button class="btn btn-login btn-success" @click="request">Отправить запрос</button>
    </form>
</div>
    
</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, email } from '@vuelidate/validators'

    export default{
        setup () {
            return {
                v$: useVuelidate()
            }
        },
        data(){
            return {
                user: {
                    login: '',
                    email: '',
                    password: '',
                    country: 'Russia',
                    agreeWithRules: false,
                },
                countries: ['Russia', 'USA', 'French'],
                accessToken: ''

            }
        },
        validations: {
            user: {
                login: { required, minLength: minLength(3) },
                email: {required, email},
                password: {required, minLength: minLength(3)},
                agreeWithRules: {
                    mustBeTrue(value){
                        return value
                    }
                },
            }
        },
        methods: {
            checkForm() {
                this.v$.user.$touch()
                if (!this.v$.user.$error) {
                    console.log('Валидация прошла успешно')
                }
                else console.log('Валидация не прошла')
            },

            created() {
                console.log('post request')
                // const newPassword = this.addUser
                // const requestOptions = {
                //       method: 'POST',
                //       headers: { 'Content-Type': 'application/json; charset=UTF-8' },
                //       body: JSON.stringify({ 'login': this.user.login, 'password': newPassword })
                //     };
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
                        // console.log(this.accessToken)
            }
        }
    }
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  margin-top: 40px;
}
.form-control {
  width: 400px;
}
.btn-login {
    width: 200px;
    align-content: center;
}

</style>