<template>
  <NuxtLink :to="`/item/${id}`" class="link-invisible">
    <b-card no-body :img-src="image || defaultImage" img-top>
      <b-card-body>
        <div class="d-flex flex-row justify-content-between">
          <b-card-title :title="name" title-tag="h5"></b-card-title>
          <div v-if="!hideCollectedStatus && collected">
            <font-awesome-icon :icon="['fas', 'check']" />
          </div>
        </div>
      </b-card-body>
    </b-card>
  </NuxtLink>
</template>

<script>
export default {
  props: {
    id: {
      default: '',
      type: String,
    },
    name: {
      default: 'Item',
      type: String,
    },
    image: {
      default: '/img/placeholder.png',
      type: String,
    },
    collected: {
      default: false,
      type: Boolean,
    },
    hideCollectedStatus: {
      default: false,
      type: Boolean,
    },
  },
  data() {
    return {
      defaultImage: '/img/placeholder.png',
    }
  },
}
</script>

<style scoped>
h5 {
  font-weight: normal;
}
.card-title {
  margin-bottom: 0px;
}
</style>
