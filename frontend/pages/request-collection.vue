<template>
  <b-container>
    <b-row align-h="center">
      <h3 class="mb-3">request a collection</h3>
      <b-col cols="12">
        <b-row align-h="center">
          <b-col class="mb-3" cols="6">
            <div>
              <label class="typo__label">Name</label>
              <b-form-input
                v-model="name"
                placeholder="Enter a name"
                type="text"
              ></b-form-input>
              <label class="typo__label">Description</label>
              <b-form-textarea
                v-model="description"
                placeholder="Enter a description"
                type="text"
              ></b-form-textarea>
              <label class="typo__label">Evidence</label>
              <b-form-textarea
                v-model="evidence"
                placeholder="Enter evidence"
                type="text"
              ></b-form-textarea>
              <b-button
                block
                class="mt-3"
                variant="collectr-primary"
                @click="requestCollection"
              >
                Request collection
              </b-button>
            </div>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      description: '',
      evidence: '',
    }
  },
  methods: {
    async requestCollection() {
      if (!this.name) {
        alert('Name is required!')
        return
      }
      if (!this.description) {
        alert('Description is required!')
        return
      }
      if (!this.evidence) {
        alert('Evidence is required!')
        return
      }
      const form = new FormData()
      form.append('requester', this.$nuxt.context.$auth.user.id)
      form.append('new_name', this.name)
      form.append('description', this.description)
      form.append('evidence', this.evidence)
      await this.$axios.$post('request/collection/', form)
      await this.$router.push(`/`)
    },
  },
}
</script>
