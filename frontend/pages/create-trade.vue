<template>
  <b-container>
    <b-row align-h="center">
      <h3 class="mb-3">create a trade</h3>
      <b-col cols="12">
        <b-row align-h="center">
          <b-col cols="6" class="mb-3">
            <div>
              <label class="typo__label">Description <i>(required)</i></label>
              <b-form-textarea
                id="input-3"
                v-model="description"
                type="text"
                placeholder="Enter a description"
              ></b-form-textarea>
            </div>
          </b-col>
        </b-row>
        <b-row align-h="center" align-v="end">
          <b-col cols="5" class="mb-3">
            <div>
              <label class="typo__label">Attachments</label>
              <b-form-file
                v-model="attachments"
                placeholder="Choose files or drop files here..."
                drop-placeholder="Drop files here..."
                accept="image/*"
                multiple
              ></b-form-file>
            </div>
          </b-col>
          <b-col cols="1" class="mb-3">
            <b-button @click="attachments = []">Clear</b-button>
          </b-col>
        </b-row>
        <b-row align-h="center">
          <b-col cols="6" class="mb-3">
            <div>
              <label class="typo__label">Collection</label>
              <multiselect
                v-model="multiselect.collection"
                :options="collections"
                :show-labels="false"
                track-by="id"
                label="title"
                placeholder="Pick a collection"
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
              <div class="mx-auto my-auto pt-4"><BoxLoader /></div>
            </template>
            <template v-else>
              <b-col cols="5">
                <div>
                  <label class="typo__label">Items to trade</label>
                  <multiselect
                    v-model="multiselect.items.have"
                    :options="items"
                    :multiple="true"
                    :close-on-select="false"
                    :clear-on-select="false"
                    :preserve-search="true"
                    open-direction="above"
                    placeholder="Choose the items you want to trade"
                    label="name"
                    track-by="id"
                    :max="6"
                  >
                  </multiselect></div
              ></b-col>
              <b-col cols="2"> </b-col>
              <b-col cols="5">
                <div>
                  <label class="typo__label">Items to receive</label>
                  <multiselect
                    v-model="multiselect.items.want"
                    :options="items"
                    :multiple="true"
                    :close-on-select="false"
                    :clear-on-select="false"
                    :preserve-search="true"
                    open-direction="above"
                    placeholder="Choose the items you want to recieve"
                    label="name"
                    track-by="id"
                    :max="6"
                  >
                  </multiselect></div
              ></b-col>
              <b-col cols="12">
                <TradeListingItems
                  :have="multiselect.items.have"
                  :want="multiselect.items.want"
                  class="mb-2"
                />
              </b-col>
              <b-col cols="4" class="mt-3">
                <b-button
                  v-if="!submitting"
                  block
                  variant="collectr-primary"
                  @click="createTrade"
                >
                  Create trade
                </b-button>
                <b-row v-else align-h="center"> <BoxLoader /></b-row>
              </b-col>
            </template>
          </template>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      collections: [],
      items: [],
      description: '',
      attachments: [],
      multiselect: {
        collection: null,
        items_loaded: false,
        items: {
          have: [],
          want: [],
        },
      },
      submitting: false,
    }
  },
  async fetch() {
    this.collections = await this.$axios.$get('collections/')
    this.collections = this.collections.filter((e) => e.item_count)
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
      this.items = collection.results.Item ?? []
      this.multiselect.items_loaded = true
    },
    async createTrade() {
      if (!this.description) {
        alert('Description is required!')
        return
      }

      if (
        !this.multiselect.items.have.length ||
        !this.multiselect.items.want.length
      ) {
        alert('Both sides of the trade must contain at least one item!')
        return
      }

      // display loading indicator while we chug through data and image uploads
      this.submitting = true
      const form = new FormData()
      form.append('creator', this.$nuxt.context.$auth.user.id)
      form.append('description', this.description)
      for (const item of this.multiselect.items.have) {
        form.append('have', item.id)
      }
      for (const item of this.multiselect.items.want) {
        form.append('want', item.id)
      }

      // BE requires images to be sent individually
      const response = await this.$axios.$post('trades/create/', form)
      for (const attachment of this.attachments) {
        const attachmentForm = new FormData()
        attachmentForm.append('trade_id', response.id)
        attachmentForm.append('attachment', attachment)
        await this.$axios.$post(
          `/trades/${response.id}/attachments/`,
          attachmentForm
        )
      }

      this.$router.push(`/trade/${response.id}/`)
    },
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
