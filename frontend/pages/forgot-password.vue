<template>
  <div class="vh-100 d-flex justify-content-center align-items-center">
    <div v-if="!email_sent" style="width: 400px">
      <div class="pb-4">
        <b-img
          src="/img/collectr-logo.svg"
          fluid
          alt="Fluid image"
          width="200"
        ></b-img>
      </div>

      <b-form @submit.stop.prevent @submit="onSubmit">
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

        <div class="pt-2">
          <b-button type="submit" variant="collectr-primary">
            Send magic link
          </b-button>
        </div>
      </b-form>
    </div>
    <div v-else>
      <b-col cols="12" class="text-center">
        <h4>Magic link sent!</h4>
      </b-col>
      <b-col cols="12" class="text-center">
        <h5>
          If an account with the provided email exists, we sent an email
          containing a magic link.<br />Please follow the link in the email to
          log into to your account, then change your password on the Edit
          Profile page.
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
        email: '',
      },
      email_sent: false,
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      const form = new FormData()
      form.append('email', this.form.email)
      this.$axios.post('auth/reset/', form).then(() => {
        this.email_sent = true
      })
    },
  },
}
</script>
