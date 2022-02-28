<template>
  <b-row align-v="center" class="py-2 px-2">
    <b-col>
      <TradeItems :items="have" in-listing />
    </b-col>
    <b-col cols="2" style="text-align: center">
      <font-awesome-icon :icon="['fas', 'exchange-alt']" class="icon" />
    </b-col>
    <b-col> <TradeItems :items="want" in-listing /> </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    inListing: {
      type: Boolean,
      default: false,
    },
    have: {
      type: Array,
      default: () => [],
    },
    want: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
