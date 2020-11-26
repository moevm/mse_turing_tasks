<template>
  <div>
    <b-container class="container" sm="5">
      <b-form @submit="onSubmit">
        <b-form-group
            id="input-group-1"
            label="Email address:"
            label-for="input-1"
            description=""
        >
          <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              required
              placeholder="Enter email"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Password:" label-for="input-2">
          <b-input
              type="password"
              id="text-password"
              aria-describedby="password-help-block"
              v-model="form.password"
              placeholder="Enter password"
          ></b-input>
        </b-form-group>

        <b-alert v-model="showError" variant="danger" dismissible>Incorrect email or password</b-alert>

        <b-button type="login"
                  variant="primary"
                  @click="onSubmit">Вход
        </b-button>
      </b-form>
      <b-button type="register"
                variant="primary"
                @click="show=true"
      >Регистрация
      </b-button>
    </b-container>

    <b-modal id="reg" v-model="show">
      <b-container class="container" sm="5">
        <b-form @submit="registerNew">
          <b-form-group
              id="input-group-register-1"
              label="Username:"
              label-for="input-1"
              description=""
          >
            <b-form-input
                id="input-1"
                v-model="form.name"
                type="text"
                required
                placeholder="Enter username"
            ></b-form-input>
          </b-form-group>
          <b-form-group
              id="input-group-register-2"
              label="Email address:"
              label-for="input-1"
              description=""
          >
            <b-form-input
                id="input-1"
                v-model="form.email"
                type="email"
                required
                placeholder="Enter email"
            ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-register-3" label="Password:" label-for="input-2">
            <b-input
                type="password"
                id="text-password"
                aria-describedby="password-help-block"
                v-model="form.password"
                placeholder="Enter password"
            ></b-input>
          </b-form-group>

          <b-alert v-model="showError" variant="danger" dismissible>Incorrect email or password</b-alert>

        </b-form>
      </b-container>

      <template #modal-footer>
        <div class="w-100">
          <b-button
              variant="primary"
              size="sm"
              class="float-right"
              @click="show=false"
          >
            Close
          </b-button>
          <b-button type="login"
                    variant="primary"
                    size="sm"
                    class="float-right"
                    @click="registerNew"
          >Зарегистрироваться
          </b-button>
        </div>
      </template>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";
import {bus} from '@/main';

export default {
  name: "Authorization",
  data() {
    return {
      show: false,
      form: {
        email: '',
        password: '',
        name: ''
      },
      showError: false,
      debugMode: false,
      api: 'https://wintari.pythonanywhere.com',
      token: ''
    }
  },
  created() {
    // this.api = `https://wintari.pythonanywhere.com`
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      if (!this.debugMode) {
        // console.log(`${this.api}/login`)
        console.log({
          email: this.form.email,
          password: this.form.password
        })
        axios.post(`${this.api}/login`, JSON.stringify({
              "email": this.form.email,
              "password": this.form.password
            }),
            {
              headers: {
                'Content-Type': 'application/json'
              }
            }
        )
            .then((res) => {
              console.log(res)
              bus.$emit('login', res.data.token)
              this.user = res.data.user;
              this.showError = false;
              localStorage.setItem('token', res.data.token);
              router.push('/main');
            })
            .catch((error) => {
                  this.form.email = '';
                  this.form.password = ''
                  this.showError = true;
                  console.error(error);
                }
            )
      } else {
        router.push('/main');
      }
    },
    registerNew() {
      if (!this.debugMode) {
        axios.post(`${this.api}/register`, {
          "email": this.form.email,
          "password": this.form.password,
          "name": this.form.name
        })
            .then((res) => {
              console.log(res)
              // this.token = res.data.user;

              this.showError = false;
              this.show = false;
            })
            .catch((error) => {
                  this.showError = true;
                  this.form.email = '';
                  this.form.password = ''
                  this.form.name = ''
                  console.error(error);
                }
            )
      } else {
        console.log('reg')
      }
    }
  }
}
</script>

<style scoped>
.container {

}
</style>
