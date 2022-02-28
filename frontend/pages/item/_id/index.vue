<template>
  <div v-if="$fetchState.pending"></div>
  <div v-else class="container">
    <div class="d-flex flex-row pb-2">
      <div class="d-flex col-3">
        <div class="d-flex flex-column">
          <b-img
            thumbnail
            fluid
            :src="item.cover_image || defaultImage"
          ></b-img>
        </div>
      </div>
      <div class="d-flex col-7">
        <div class="d-flex flex-column">
          <div class="d-flex flex-row justify-content-around">
            <div class="d-flex flex-column">
              <h3>{{ item.name }}</h3>
              <h5>
                Part of
                <NuxtLink
                  :to="`/collection/${collection.id}`"
                  class="link-collectr"
                  >{{ collection.title }}</NuxtLink
                >
              </h5>
              <div
                v-if="item.collected"
                class="d-flex flex-row align-items-baseline"
              >
                <font-awesome-icon :icon="['fas', 'check']" />
                <h6 class="ml-2">This item is in your collection</h6>
              </div>
              <div v-else class="d-flex flex-row align-items-baseline">
                <font-awesome-icon :icon="['fas', 'times']" />
                <h6 class="ml-2">This item is not in your collection</h6>
              </div>
              <p>
                <b>Release date:</b>
                {{
                  item.release_date
                    ? $moment(new Date(item.release_date)).format('MMM Do YYYY')
                    : 'Unknown'
                }}
              </p>
              <p><b>Description:</b> {{ item.description }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex col-2">
        <div class="d-flex flex-column">
          <b-button
            id="confetti"
            block
            variant="collectr-primary"
            :disabled="submitting"
            @click="toggleCollected"
            >{{ collectionToggleButton }}</b-button
          >
        </div>
      </div>
    </div>
  </div>
</template>
``

<script>
import confettiCannon from 'canvas-confetti'

const count = 200
const defaults = {
  origin: { x: 0.5, y: 0.1 },
}

function fire(particleRatio, opts) {
  confettiCannon(
    Object.assign({}, defaults, opts, {
      particleCount: Math.floor(count * particleRatio),
    })
  )
}

function confetti() {
  fire(0.25, {
    spread: 26,
    startVelocity: 55,
  })
  fire(0.2, {
    spread: 60,
  })
  fire(0.35, {
    spread: 100,
    decay: 0.91,
    scalar: 0.8,
  })
  fire(0.1, {
    spread: 120,
    startVelocity: 25,
    decay: 0.92,
    scalar: 1.2,
  })
  fire(0.1, {
    spread: 120,
    startVelocity: 45,
  })
}

export default {
  data() {
    return {
      fullCollection: {},
      collection: {},
      item: {},
      collected: false,
      submitting: false,
      defaultImage: '/img/placeholder.png',
    }
  },
  async fetch() {
    this.item = await this.$axios.$get(`item/${this.$nuxt.context.params.id}/`)
    const response = await this.$axios.$get(
      `collections/${this.item.collection}/`
    )
    this.collection = response.results.Collection[0]
    await this.refetchItemData()
  },
  fetchDelay: 500,
  computed: {
    collectionToggleButton() {
      return this.item.collected
        ? 'Remove from collection'
        : 'Add to collection'
    },
  },
  methods: {
    async toggleCollected() {
      this.submitting = true
      const form = new FormData()
      form.append('user', this.$nuxt.context.$auth.user.id)
      form.append('item_id', this.item.id)
      if (!this.item.collected) {
        confetti()
        await this.$axios.$post(
          `collect/${this.$nuxt.context.$auth.user.id}/${this.item.id}/`,
          form
        )
      } else {
        await this.$axios.$delete(
          `collect/${this.$nuxt.context.$auth.user.id}/${this.item.id}/`,
          form
        )
      }
      await this.refetchItemData()
      this.submitting = false
    },
    async refetchItemData() {
      this.item = await this.$axios.$get(
        `item/${this.$nuxt.context.params.id}/`
      )
      this.fullCollection = await this.$axios.$get(
        `collections/${this.collection.id}/`
      )
      this.collection = this.fullCollection.results.Collection[0]
    },
  },
}
</script>
