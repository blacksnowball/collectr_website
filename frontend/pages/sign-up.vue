<template>
  <div class="vh-100 d-flex justify-content-center align-items-center">
    <div v-if="!registered" style="width: 400px">
      <div class="pb-4">
        <b-img
          src="/img/collectr-logo.svg"
          fluid
          alt="Fluid image"
          width="200"
        ></b-img>
      </div>

      <b-form @submit.stop.prevent @submit="onSubmit">
        <b-form-group id="input-group-1" label="Username:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.username"
            placeholder="Enter username"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-2"
          label="Email address:"
          label-for="input-2"
        >
          <b-form-input
            id="input-2"
            v-model="form.email"
            type="email"
            placeholder="Enter email address"
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
        </b-form-group>

        <b-form-group
          id="input-group-4"
          label="Confirm password:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="form.confirm_password"
            :state="validatePasswordMatch"
            type="password"
            placeholder="Re-enter password"
            required
          ></b-form-input>
          <b-form-invalid-feedback :state="validatePasswordMatch">
            Password does not match!
          </b-form-invalid-feedback>
        </b-form-group>

        <div class="pt-2">
          <b-button type="submit" variant="collectr-primary">
            Create account
          </b-button>
        </div>

        <div class="pt-3">
          <p>
            Already have an account?
            <NuxtLink to="/login">Log in</NuxtLink>
          </p>
        </div>
      </b-form>
    </div>
    <div v-else>
      <b-col cols="12" class="text-center">
        <h4>Confirmation email sent!</h4>
      </b-col>
      <b-col cols="12" class="text-center">
        <h5>
          Please check your inbox and follow the link inside the confirmation
          email.
        </h5>
      </b-col>
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
        email: '',
        password: '',
        confirm_password: '',
      },
      registered: false,
    }
  },
  computed: {
    validatePasswordMatch() {
      return this.form.password && this.form.confirm_password
        ? this.form.password === this.form.confirm_password
        : null
    },
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      const form = new FormData()
      form.append('username', this.form.username)
      form.append('email', this.form.email)
      form.append('password', this.form.confirm_password)
      form.append('password2', this.form.confirm_password)
      // register and then show user the "confirm email" message
      this.$axios
        .post('auth/register/', form)
        .then(() => {
          this.registered = true
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
