<template>
  <div class="container">
    <div class="d-flex flex-column">
      <div
        v-if="$fetchState.pending"
        style="margin-bottom: 2rem"
        height="100px"
      >
        <b-skeleton-img no-aspect height="267px"></b-skeleton-img>
      </div>
      <div v-else>
        <CollectionHero :collection="collection" />
      </div>
    </div>
    <b-tabs
      content-class="mt-3"
      justified
      active-nav-item-class="font-weight-bold"
    >
      <b-tab title="All items" title-link-class="link-collectr">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto"><BoxLoader /></div>
        </div>
        <div v-else class="row row-cols-5 mt-4">
          <div v-for="item in items" :key="item.id" class="col mb-4">
            <ItemCard
              :id="item.id"
              :name="item.name"
              :image="item.cover_image"
              :collected="item.collected"
            />
          </div>
        </div>
      </b-tab>
      <b-tab title="My items" title-link-class="link-collectr">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto"><BoxLoader /></div>
        </div>
        <div v-else class="row row-cols-5 mt-4">
          <div v-for="item in userItems" :key="item.id" class="col mb-4">
            <ItemCard
              :id="item.id"
              :name="item.name"
              :image="item.cover_image"
              :collected="item.collected"
            />
          </div>
        </div>
      </b-tab>
    </b-tabs>

    <b-button block class="my-3" variant="collectr-primary" to="/request-item">
      Request item
    </b-button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      collection: {},
      items: [],
      userItems: [],
    }
  },
  async fetch() {
    const response = await this.$axios.$get(
      `collections/${this.$nuxt.context.params.id}/`
    )
    this.collection = response.results.Collection[0]
    this.items = response.results.Item
    this.userItems = await this.$axios.$get(
      `collections/${this.$nuxt.context.params.id}/mine/`
    )
  },
  fetchDelay: 500,
}
</script>
