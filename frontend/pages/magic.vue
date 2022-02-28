<template>
  <!-- Magic link handling - if user has valid link, log them in and ask them to change password -->
  <div class="vh-100 d-flex justify-content-center align-items-center">
    <template v-if="invalid">
      <b-col cols="12" class="pb-4 px-0 text-center">
        <h4>Invalid password reset link. Please try again.</h4>
      </b-col>
    </template>
    <template v-else-if="success">
      <b-col cols="12" class="pb-4 px-0 text-center">
        <h4>Account confirmed. Redirecting...</h4>
      </b-col>
    </template>
    <template v-else>
      <b-row align-h="center">
        <b-col cols="12" class="pb-4 px-0 text-center">
          <h4>Confirming your account, give us a second...</h4>
        </b-col>
        <b-col cols="12" class="text-center">
          <BoxLoader />
        </b-col>
      </b-row>
    </template>
  </div>
</template>

<script>
export default {
  auth: 'guest',
  layout: 'empty',
  data() {
    return {
      invalid: false,
      success: false,
    }
  },
  mounted() {
    // make sure user has a token!
    const token = this.$route.query.token
    if (!token) {
      this.invalid = true
      return
    }
    this.tryConfirmation(token)
  },
  methods: {
    async tryConfirmation(token) {
      await this.$axios
        .get(`auth/reset_ok/?token=${token}`)
        .then(async (response) => {
          this.success = true
          // use auth plugin to update token info
          await this.$auth.setUserToken(
            response.data.access,
            response.data.refresh
          )
        })
        .catch(() => {
          this.invalid = true
        })
    },
  },
}
</script>
