<template>
<div class="container login">
<!--    <form>-->
      <form @submit.prevent="created">
        <div class="form-group">
            <label>Login: </label>
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
            <label >Password: </label>
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
            <button type="submit" class="btn btn-primary col-auto">Войти</button>

<!--            <button class="btn btn-success col-auto" @click="request">Отправить запрос</button>-->
        </div>
    </form>
  <button @click="post">register</button>
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
                autorized: false,
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
              // console.log('check')
               this.v$.user.$touch()
                if (!this.v$.user.$error) {
                    console.log('Валидация прошла успешно')
                  if (this.accessLogin === true){
                    console.log('check')
                    this.autorized = true
                    this.$emit('sendLogin', this.autorized)
                  }
                }
                else console.log('Валидация не прошла')
            },
            created() {
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

                          if (response.login === true){
                            this.accessLogin = true
                            // this.post()
                            this.checkForm()
                          }
                        });
            },
          post(){
            fetch('http://localhost:5000/getTasks', {
              method: 'POST',
              credentials:"include",
              cors: 'no-cors',
              headers: {
                'Content-Type': 'application/json;charset=utf-8',
              },
              body:JSON.stringify({"date": "08/30/2023"})
            })
                .then(response => response.json())
                .then(response => {
                  console.log(response)
                })
          },
          register() {
            fetch('http://localhost:5000/register', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json;charset=utf-8',
              },
              body: JSON.stringify({'name': "name",
                "surname": 'surname',
                "login" : 'login',
                "password" : "password"})
            })
                .then((response) => {
                  console.log(response.json())
                });
          },
            request() {
                fetch('http://192.168.43.243:5000/getTestData', {
                          method: 'POST',
                          credentials: "include",
                          headers: {
                            // 'Authentication': 'Bearer {' + this.accessToken +'}',
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