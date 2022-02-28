<template>
  <div class="container">
    <div style="text-align: center">
      <h3 class="mb-3">requests</h3>
    </div>
    <b-tabs
      v-if="$auth.user.is_staff"
      active-nav-item-class="font-weight-bold"
      content-class="mt-3"
      justified
    >
      <b-tab title="Item Requests" title-link-class="link-collectr">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto">
            <BoxLoader />
          </div>
        </div>
        <div v-else class="mt-4">
          <div v-if="!itemRequests.length" style="text-align: center">
            <p>There are no item requests.</p>
          </div>
          <div v-else>
            <div
              v-for="itemRequest in itemRequests"
              :key="itemRequest.id"
              class="col mb-4"
            >
              <b-card no-body>
                <b-card-body>
                  <div class="d-flex flex-row justify-content-between">
                    <div>
                      <b-card-title
                        :title="itemRequest.new_name"
                      ></b-card-title>
                    </div>
                  </div>
                  <b-card-text
                    >Collection:
                    <NuxtLink
                      :to="`/collection/${itemRequest.add_to_collection}`"
                    >
                      {{ itemRequest.collection.title }}
                    </NuxtLink></b-card-text
                  >
                  <b-card-text
                    >Description: {{ itemRequest.description }}</b-card-text
                  >
                  <b-card-text
                    >Evidence: {{ itemRequest.evidence }}</b-card-text
                  >
                  <b-button
                    variant="collectr-primary"
                    @click="actionItemRequest(itemRequest, true)"
                    >Approve
                  </b-button>
                  <b-button
                    variant="collectr-secondary"
                    @click="actionItemRequest(itemRequest, false)"
                    >Deny
                  </b-button>
                </b-card-body>
              </b-card>
            </div>
          </div>
        </div>
      </b-tab>
      <b-tab title="Collection Requests" title-link-class="link-collectr">
        <div v-if="$fetchState.pending" class="d-flex pt-4">
          <div class="mx-auto my-auto">
            <BoxLoader />
          </div>
        </div>
        <div v-else class="mt-4">
          <div v-if="!collectionRequests.length" style="text-align: center">
            <p>There are no collection requests.</p>
          </div>
          <div v-else>
            <div
              v-for="collectionRequest in collectionRequests"
              :key="collectionRequest.id"
              class="col mb-4"
            >
              <b-card no-body>
                <b-card-body>
                  <div class="d-flex flex-row justify-content-between">
                    <div>
                      <b-card-title
                        :title="collectionRequest.new_name"
                      ></b-card-title>
                    </div>
                  </div>
                  <b-card-text
                    >Description:
                    {{ collectionRequest.description }}</b-card-text
                  >
                  <b-card-text
                    >Evidence: {{ collectionRequest.evidence }}</b-card-text
                  >
                  <b-button
                    variant="collectr-primary"
                    @click="actionCollectionRequest(collectionRequest, true)"
                  >
                    Approve
                  </b-button>
                  <b-button
                    variant="collectr-secondary"
                    @click="actionCollectionRequest(collectionRequest, false)"
                  >
                    Deny
                  </b-button>
                </b-card-body>
              </b-card>
            </div>
          </div>
        </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      collections: [],
      itemRequests: [],
      collectionRequests: [],
    }
  },
  async fetch() {
    await this.refetchRequests()
  },
  fetchDelay: 500,
  methods: {
    async actionItemRequest(request, approve) {
      const form = new FormData()
      form.append('id', request.id)
      form.append('new_name', request.new_name)
      form.append('description', request.description)
      form.append('requester', request.requester)
      form.append('evidence', request.evidence)
      form.append('add_to_collection', request.add_to_collection)
      form.append('isApproved', approve)
      await this.$axios.post(`request/item/${request.id}/`, form)
      await this.refetchRequests()
    },
    async actionCollectionRequest(request, approve) {
      const form = new FormData()
      form.append('id', request.id)
      form.append('new_name', request.new_name)
      form.append('requester', request.requester)
      form.append('description', request.description)
      form.append('evidence', request.evidence)
      form.append('isApproved', approve)
      await this.$axios.post(`request/collection/${request.id}/`, form)
      await this.refetchRequests()
    },
    async refetchRequests() {
      this.collections = await this.$axios.$get('collections/')
      const itemReqs = await this.$axios.$get('request/item/')
      this.itemRequests = itemReqs
      this.itemRequests.forEach((req) => {
        req.collection = this.collections.find(
          (coll) => coll.id === req.add_to_collection
        )
      })
      const collReqs = await this.$axios.$get('request/collection/')
      this.collectionRequests = collReqs
    },
  },
}
</script>
