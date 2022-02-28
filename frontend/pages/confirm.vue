<template>
  <!-- Asks BE to enable user account and then lets them log in -->
  <div class="vh-100 d-flex justify-content-center align-items-center">
    <b-row align-h="center">
      <template v-if="invalid">
        <b-col cols="12" class="pb-4 px-0 text-center">
          <h4>Invalid confirmation link. Please try again.</h4>
        </b-col>
      </template>
      <template v-else-if="success">
        <b-col cols="12" class="pb-4 px-0 text-center">
          <h4>Account confirmed! Please log in.</h4>
        </b-col>
        <b-col cols="12" class="text-center">
          <b-button variant="collectr-primary" to="/login"> Log in </b-button>
        </b-col>
      </template>
      <template v-else>
        <b-col cols="12" class="pb-4 px-0 text-center">
          <h4>Confirming your account, give us a second...</h4>
        </b-col>
        <b-col cols="12" class="text-center">
          <BoxLoader />
        </b-col>
      </template>
    </b-row>
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
        .get(`auth/register_done/?token=${token}`)
        .then(() => {
          this.success = true
        })
        .catch(() => {
          this.invalid = true
        })
    },
  },
}
</script>
