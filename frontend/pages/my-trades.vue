<template>
  <b-container>
    <b-row align-h="center">
      <h3 class="mb-3">my trades</h3>
      <b-col cols="12">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto"><BoxLoader /></div>
        </div>
        <div v-else>
          <div v-if="trades.length === 0">
            <b-row align-h="center" class="mt-3"
              ><p>You don't have any trades yet!</p></b-row
            >
            <b-row align-h="center"
              ><b-button variant="collectr-primary" to="/create-trade">
                Create a trade
              </b-button></b-row
            >
          </div>

          <div v-else>
            <NuxtLink
              v-for="trade in trades"
              :key="trade.id"
              :to="`/trade/${trade.id}`"
              class="link-invisible-no-hover"
            >
              <TradeListing :trade="trade" class="mb-3" />
            </NuxtLink>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      trades: [],
    }
  },
  async fetch() {
    this.trades = await this.$axios.$get(
      `${this.$nuxt.context.$auth.user.id}/trades/`
    )
  },
  fetchDelay: 500,
}
</script>
