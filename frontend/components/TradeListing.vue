<template>
  <b-row :class="{ listing: trade.active, listing_closed: !trade.active }">
    <b-col>
      <b-row class="inner-listing py-2">
        <b-col>
          {{ trade.creator.username }}
          <b>{{ !trade.active ? '(CLOSED)' : '' }}</b>
        </b-col>
        <b-col style="text-align: right">
          {{ $moment(trade.creation_date).fromNow() }}
        </b-col>
      </b-row>
      <TradeListingItems :have="trade.have" :want="trade.want" in-listing />
    </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    trade: {
      default: () => {},
      type: Object,
    },
  },
}
</script>

<style scoped lang="scss">
@import '/assets/scss/variables.scss';

$closed-color: $collectr-tertiary;
$border-color: #d3d3d3;
$border-definition: 1px solid $border-color;

.listing {
  border: $border-definition;
  border-radius: 5px;
}
.listing_closed {
  border: $border-definition;
  border-radius: 5px;
  background-color: $closed-color;
}
.inner-listing {
  border-bottom: $border-definition;
}
.icon {
  color: $collectr-secondary;
  font-size: 4vw;
}
</style>
