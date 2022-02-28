<template>
  <b-container>
    <b-row v-if="search === false" align-h="center">
      <h3 class="mb-3">search for trade</h3>
      <b-col cols="12">
        <b-row align-h="center">
          <b-col class="mb-3" cols="6">
            <div>
              <label class="typo__label">Description</label>
              <b-form-textarea
                id="input-2"
                v-model="description"
                placeholder="Enter a description"
                type="text"
              ></b-form-textarea>
            </div>
          </b-col>
        </b-row>
        <b-row align-h="center">
          <b-col class="mb-3" cols="6">
            <div>
              <label class="typo__label">Creator</label>
              <b-form-input
                id="input-3"
                v-model="creator"
                placeholder="Enter creator username"
                type="text"
              ></b-form-input>
            </div>
          </b-col>
        </b-row>
        <b-row align-h="center">
          <b-col class="mb-3" cols="6">
            <div>
              <label class="typo__label">Collection</label>
              <multiselect
                v-model="multiselect.collection"
                :options="collections"
                :show-labels="false"
                label="title"
                placeholder="Pick a collection"
                track-by="id"
                @input="loadItems"
              ></multiselect>
            </div>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <b-row align-h="center">
          <template v-if="multiselect.collection != null">
            <template v-if="!multiselect.items_loaded">
              <div class="mx-auto my-auto pt-4">
                <BoxLoader />
              </div>
            </template>
            <template v-else>
              <b-col cols="5">
                <div>
                  <label class="typo__label">Have</label>
                  <multiselect
                    v-model="multiselect.items.have"
                    :clear-on-select="false"
                    :close-on-select="false"
                    :max="6"
                    :multiple="true"
                    :options="items"
                    :preserve-search="true"
                    label="name"
                    open-direction="above"
                    placeholder="Choose the items you want to trade"
                    track-by="id"
                  >
                  </multiselect>
                </div>
              </b-col>
              <b-col cols="2"></b-col>
              <b-col cols="5">
                <div>
                  <label class="typo__label">Want</label>
                  <multiselect
                    v-model="multiselect.items.want"
                    :clear-on-select="false"
                    :close-on-select="false"
                    :max="6"
                    :multiple="true"
                    :options="items"
                    :preserve-search="true"
                    label="name"
                    open-direction="above"
                    placeholder="Choose the items you want to recieve"
                    track-by="id"
                  >
                  </multiselect>
                </div>
              </b-col>
              <b-col cols="12">
                <TradeListingItems
                  :have="multiselect.items.have"
                  :want="multiselect.items.want"
                  class="mb-2"
                />
              </b-col>
              <b-col class="my-3" cols="4">
                <b-button block variant="collectr-primary" @click="getTrades">
                  Search trades
                </b-button>
              </b-col>
            </template>
          </template>
        </b-row>
      </b-col>
    </b-row>
    <b-row v-else align-h="center">
      <b-col cols="12" style="text-align: center">
        <h3 class="mb-3">search results</h3>
      </b-col>
      <b-col class="my-3" cols="4">
        <b-button block variant="collectr-primary" @click="resetSearch">
          Search again
        </b-button>
      </b-col>
      <NuxtLink
        v-for="trade in trades"
        :key="trade.id"
        :to="`/trade/${trade.id}`"
        class="link-invisible-no-hover"
      >
        <TradeListing :trade="trade" class="mb-3" />
      </NuxtLink>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      search: false,
      collections: [],
      items: [],
      trades: [],
      description: '',
      creator: '',
      multiselect: {
        collection: null,
        items_loaded: false,
        items: {
          have: [],
          want: [],
        },
      },
    }
  },
  async fetch() {
    const collections = await this.$axios.$get('/collections/')
    this.collections = collections
  },
  methods: {
    async loadItems() {
      if (this.multiselect.collection == null) {
        this.items = []
        return
      }

      // reset previous
      this.multiselect.items.have = []
      this.multiselect.items.want = []
      this.multiselect.items_loaded = false

      const collection = await this.$axios.$get(
        `/collections/${this.multiselect.collection.id}/`
      )
      this.items = collection.results.Item
      this.multiselect.items_loaded = true
    },
    async getTrades() {
      let query = '/trades/'
      let separator = '?'

      if (this.description) {
        query = query.concat(`${separator}description=${this.description}`)
        separator = '&'
      }
      if (this.creator) {
        query = query.concat(`${separator}creator=${this.creator}`)
        separator = '&'
      }
      if (this.multiselect.items.have.length) {
        const itemstring = this.multiselect.items.have
          .map((item) => item.id)
          .join(',')
        query = query.concat(`${separator}have=${itemstring}`)
        separator = '&'
      }
      if (this.multiselect.items.want.length) {
        const itemstring = this.multiselect.items.want
          .map((item) => item.id)
          .join(',')
        query = query.concat(`${separator}want=${itemstring}`)
        separator = '&'
      }

      const response = await this.$axios.$get(query)
      this.trades = response
      this.search = true
    },
    resetSearch() {
      this.search = false
    },
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
