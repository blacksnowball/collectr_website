<template>
  <div class="container">
    <div style="text-align: center">
      <h3 class="mb-3">collections</h3>
    </div>

    <b-tabs
      active-nav-item-class="font-weight-bold"
      content-class="mt-3"
      justified
    >
      <b-tab title="All collections" title-link-class="link-collectr">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto">
            <BoxLoader />
          </div>
        </div>
        <div v-else class="row row-cols-4 mt-4">
          <div
            v-for="collection in collections"
            :key="collection.id"
            class="col mb-4"
          >
            <CollectionCard
              :id="collection.id"
              :collected-count="collection.collected_count"
              :image="collection.thumbnail"
              :item-count="collection.item_count"
              :name="collection.title"
            />
          </div>
        </div>
      </b-tab>
      <b-tab title="My collections" title-link-class="link-collectr">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto">
            <BoxLoader />
          </div>
        </div>
        <div v-else class="row row-cols-4 mt-4">
          <div
            v-for="collection in userCollections"
            :key="collection.id"
            class="col mb-4"
          >
            <CollectionCard
              :id="collection.id"
              :collected-count="collection.collected_count"
              :image="collection.thumbnail"
              :item-count="collection.item_count"
              :name="collection.title"
            />
          </div>
        </div>
      </b-tab>
    </b-tabs>

    <b-button
      block
      class="my-3"
      variant="collectr-primary"
      to="/request-collection"
    >
      Request collection
    </b-button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      collections: [],
      userCollections: [],
    }
  },
  async fetch() {
    this.collections = await this.$axios.$get('collections/')
    this.userCollections = await this.$axios.$get('collections/mine/')
  },
  fetchDelay: 500,
}
</script>
