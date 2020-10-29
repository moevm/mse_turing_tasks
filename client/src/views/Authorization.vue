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

        <b-button type="submit" variant="primary">Submit</b-button>
      </b-form>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";

export default {
  name: "Authorization",
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      showError: false,
      debugMode: true
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      // alert(JSON.stringify(this.form))
      const path = 'http:/localhost:5000/something_address';
      if (!this.debugMode) {
        axios.get(path)
            .then((res) => {
              this.user = res.data.user;
              this.showError = false;
              router.push('/main');
            })
            .catch((error) => {
                  this.showError = true;
                  console.error(error);
                }
            )
      } else {
        router.push('/main');
      }
    }
  }
}
</script>

<style scoped>
.container {

}
</style>