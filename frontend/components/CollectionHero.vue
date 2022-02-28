<template>
  <b-jumbotron :style="styles" fluid text-variant="white" class="text-center">
    <template #header
      ><b>{{ collection.title }}</b></template
    >
    <template #lead
      ><b>{{ `${collection.item_count} items total` }}</b></template
    >
  </b-jumbotron>
</template>

<script>
export default {
  props: {
    collection: {
      default: () => {},
      type: Object,
    },
  },
  computed: {
    styles() {
      return {
        background: `linear-gradient(rgba(94, 5, 126, 0.3),rgba(94, 5, 126, 0.3)), url(${this.collection.cover_image}) center center / cover no-repeat`,
      }
    },
  },
}
</script>
