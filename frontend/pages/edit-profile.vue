<template>
  <div class="d-flex justify-content-center">
    <div style="width: 400px">
      <b-form @submit="onSubmit" @submit.stop.prevent>
        <h3 class="mb-3">profile</h3>
        <b-form-group id="input-group-3" label="About:" label-for="input-3">
          <b-form-textarea
            id="input-3"
            v-model="form.about"
            :placeholder="$auth.user.about"
            max-rows="6"
            rows="3"
          ></b-form-textarea>
        </b-form-group>

        <h3 class="mb-3">settings</h3>
        <b-form-group
          id="input-group-5"
          label="New password:"
          label-for="input-5"
        >
          <b-form-input
            id="input-5"
            v-model="form.new_password"
            placeholder="Enter new password"
            type="password"
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-6"
          label="Confirm new password:"
          label-for="input-6"
        >
          <b-form-input
            id="input-6"
            v-model="form.confirm_new_password"
            :state="validatePasswordMatch"
            placeholder="Re-enter new password"
            type="password"
          ></b-form-input>
          <b-form-invalid-feedback :state="validatePasswordMatch">
            Password does not match!
          </b-form-invalid-feedback>
        </b-form-group>
        <div class="pt-2">
          <b-button type="submit" variant="collectr-primary">
            Update account
          </b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'none',
  data({ $auth }) {
    return {
      form: {
        about: $auth.user.about,
        new_password: null,
        confirm_new_password: null,
      },
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
    async onSubmit(event) {
      event.preventDefault()

      const form = new FormData()
      form.append('about', this.form.about)
      await this.$axios.patch('auth/edit/', form).catch((error) => {
        this.firstError(error.response.data)
      })

      if (this.form.confirm_new_password) {
        const form = new FormData()
        form.append('password', this.form.new_password)
        form.append('password2', this.form.confirm_new_password)
        await this.$axios.put('auth/reset_done/', form).catch((error) => {
          this.firstError(error.response.data)
        })
      }

      await this.$auth.fetchUser()
      this.$router.push(`/profile/${this.$auth.user.username}/`)
    },
    firstError(data) {
      const key = Object.keys(data)[0]
      alert(data[key][0])
    },
  },
}
</script>
