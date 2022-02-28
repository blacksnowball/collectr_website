<template>
  <div class="vh-100 d-flex justify-content-center align-items-center">
    <div style="width: 400px">
      <div class="pb-4">
        <b-img
          src="/img/collectr-logo.svg"
          fluid
          alt="Fluid image"
          width="200"
        ></b-img>
      </div>

      <b-form @submit.stop.prevent @submit="login">
        <b-form-group id="input-group-1" label="Username:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.username"
            placeholder="Enter username"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-3" label="Password:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            required
          ></b-form-input>
          <div class="pt-2">
            <p>
              <NuxtLink to="/forgot-password">Forgot password?</NuxtLink>
            </p>
          </div>
        </b-form-group>

        <div class="pt-2">
          <b-button type="submit" variant="collectr-primary"> Log in </b-button>
        </div>

        <div class="pt-3">
          <p>
            Don't have an account yet?
            <NuxtLink to="/sign-up">Sign up</NuxtLink>
          </p>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
export default {
  auth: 'guest',
  layout: 'empty',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    }
  },
  methods: {
    async login() {
      const form = new FormData()
      form.append('username', this.form.username)
      form.append('password', this.form.password)
      // login using nuxt auth plugin
      await this.$auth
        .loginWith('local', {
          data: form,
        })
        .catch((error) => {
          this.firstError(error.response.data)
        })
    },
    firstError(data) {
      const key = Object.keys(data)[0]
      alert(data[key][0])
    },
  },
}
</script>
