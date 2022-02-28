<template>
  <b-container>
    <b-row>
      <b-col cols="12">
        <b-row align-h="end" class="mb-3"
          ><b-button to="/create-trade" variant="collectr-primary">
            Create a trade
          </b-button></b-row
        >
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto"><BoxLoader /></div>
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
    const response = await this.$axios.$get('trades/')
    this.trades = response.results
  },
  fetchDelay: 500,
}
</script>
