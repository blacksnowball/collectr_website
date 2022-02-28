<template>
  <div>
    <b-navbar class="shadow-sm mb-3">
      <NuxtLink to="/">
        <b-navbar-brand class="pt-0">
          <img src="/img/collectr-logo.svg" height="20px" />
        </b-navbar-brand>
      </NuxtLink>
      <b-navbar-nav>
        <b-nav-item to="/"> Home </b-nav-item>
        <b-nav-item :to="'/profile/' + $auth.user.username">
          Profile
        </b-nav-item>
        <b-nav-item to="/collections"> Collections </b-nav-item>
        <b-nav-item-dropdown text="Trades" right>
          <b-dropdown-item to="/create-trade">Create Trade</b-dropdown-item>
          <b-dropdown-item to="/search-trades">Search Trades</b-dropdown-item>
          <b-dropdown-item to="/bookmarked-trades"
            >Bookmarked Trades</b-dropdown-item
          >
          <b-dropdown-item to="/my-trades">My Trades</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item v-if="$auth.user.is_staff" to="/requests">
          Requests
        </b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-button size="sm" variant="collectr-primary" @click="logout">
          Log Out
          <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="ml-1" />
        </b-button>
      </b-navbar-nav>
    </b-navbar>
    <Nuxt />
  </div>
</template>

<script>
export default {
  methods: {
    async logout() {
      const form = new FormData()
      form.append('refresh', this.$auth.strategy.refreshToken.get())
      await this.$auth.logout({
        data: form,
      })
    },
  },
}
</script>
