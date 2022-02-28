<template>
  <NuxtLink :to="`/collection/${id}`" class="link-invisible">
    <b-card no-body :img-src="image || defaultImage" img-top>
      <b-card-body>
        <div class="d-flex flex-row justify-content-between">
          <div><b-card-title :title="name"></b-card-title></div>
          <div v-if="itemCount !== 0 && itemCount === collectedCount">
            <font-awesome-icon :icon="['fas', 'check']" />
          </div>
          <div v-else-if="collectedCount > 0">
            <font-awesome-icon :icon="['fas', 'hourglass-half']" />
          </div>
        </div>
        <b-card-text>{{ itemCount }} items</b-card-text>
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
      default: 'Collection',
      type: String,
    },
    image: {
      default: '/img/placeholder.png',
      type: String,
    },
    itemCount: {
      default: 0,
      type: Number,
    },
    collectedCount: {
      default: 0,
      type: Number,
    },
  },
  data() {
    return {
      defaultImage: '/img/placeholder.png',
    }
  },
}
</script>
