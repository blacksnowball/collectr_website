<template>
  <b-container v-if="!$fetchState.pending">
    <b-row no-gutters>
      <b-col md="auto">
        <b-row no-gutters align-h="center">
          <b-img
            src="/img/collectr-box.svg"
            center
            class="px-4"
            rounded="circle"
          ></b-img>
        </b-row>
        <b-row class="pt-3" no-gutters variant="collectr-primary">
          <div class="mx-auto">
            {{ profileUser.username }}
          </div>
        </b-row>
        <div class="pt-3 mx-auto" style="text-align: center">
          <b-button
            v-if="isOwnProfile"
            align-self="center"
            to="/edit-profile"
            variant="collectr-primary"
          >
            Edit Profile
          </b-button>
        </div>
      </b-col>
      <b-col>
        <b-tabs active-nav-item-class="font-weight-bold" content-class="mt-3">
          <b-tab title="Info" title-link-class="link-collectr">
            <p><b>Username: </b>{{ profileUser.username }}</p>
            <p><b>Email: </b>{{ profileUser.email }}</p>
            <p v-if="profileUser.about !== ''">
              <b>About: </b>{{ profileUser.about }}
            </p>
            <p v-else>
              <b>About: </b>
              {{ isOwnProfile ? "You haven't" : "This user hasn't" }} provided a
              blurb.
            </p>
          </b-tab>
          <b-tab title="Items" title-link-class="link-collectr">
            <div v-if="profile.my_items.length">
              <div class="row row-cols-4 mt-4">
                <div
                  v-for="item in profile.my_items"
                  :key="item.id"
                  class="col mb-4"
                >
                  <ItemCard
                    :id="item.id"
                    :name="item.name"
                    :image="item.cover_image"
                  />
                </div>
              </div>
            </div>
            <div v-else>
              <p>
                {{ isOwnProfile ? "You don't" : "This user doesn't" }} have any
                items.
              </p>
            </div>
          </b-tab>
          <b-tab title="Reputation" title-link-class="link-collectr">
            <div v-if="!isOwnProfile && !hasGivenFeedback">
              <b-form-textarea
                id="input-3"
                v-model="comment_input"
                class="mb-1 p-1"
              ></b-form-textarea>
              <b-button
                block
                variant="collectr-primary"
                class="mb-3"
                @click="postComment"
              >
                Post comment
              </b-button>
            </div>
            <div v-if="profile.reputations.length">
              <div
                v-for="reputation in profile.reputations"
                :key="reputation.id"
                class="col mb-4"
              >
                <b-card :title="reputation.sender.username" class="mb-2">
                  <b-card-text>{{ reputation.comment }}</b-card-text>
                  <b-card-text>
                    {{
                      `${$moment(new Date(reputation.timestamp)).format(
                        'MMM Do YYYY'
                      )} (${$moment(new Date(reputation.timestamp)).fromNow()})`
                    }}</b-card-text
                  >
                  <b-card-text v-if="isOwnProfile">
                    <b-button
                      block
                      variant="collectr-primary"
                      class="mb-3"
                      @click="postComment"
                    >
                      Report comment
                    </b-button></b-card-text
                  >
                </b-card>
              </div>
            </div>
            <div v-else>
              <p>
                {{ isOwnProfile ? "You don't" : "This user doesn't" }} have any
                reputation comments.
              </p>
            </div>
          </b-tab>
          <b-tab title="Trades" title-link-class="link-collectr">
            <div v-if="profile.my_trades.length">
              <div
                v-for="trade in profile.my_trades"
                :key="trade.id"
                class="col mb-4"
              >
                <NuxtLink
                  :to="`/trade/${trade.id}`"
                  class="link-invisible-no-hover"
                >
                  <TradeListing :trade="trade" class="mb-3" />
                </NuxtLink>
              </div>
            </div>
            <div v-else>
              {{ isOwnProfile ? "You don't" : "This user doesn't" }} have any
              trades.
            </div>
          </b-tab>
          <b-tab title="Bookmarked Trades" title-link-class="link-collectr">
            <div v-if="profile.bookmarked_trades.length">
              <div
                v-for="trade in profile.bookmarked_trades"
                :key="trade.id"
                class="col mb-4"
              >
                <NuxtLink
                  :to="`/trade/${trade.id}`"
                  class="link-invisible-no-hover"
                >
                  <TradeListing :trade="trade" class="mb-3" />
                </NuxtLink>
              </div>
            </div>
            <div v-else>
              {{ isOwnProfile ? "You don't" : "This user doesn't" }} have any
              bookmarked trades.
            </div>
          </b-tab>
        </b-tabs>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      profile: {},
      profileUser: {},
      comment_input: '',
    }
  },
  async fetch() {
    await this.fetchProfileInfo()
  },
  computed: {
    isOwnProfile() {
      return this.$auth.user.username === this.profileUser.username
    },
    hasGivenFeedback() {
      return this.profile.reputations.some(
        (rep) => rep.sender.id === this.$auth.user.id
      )
    },
  },
  methods: {
    async fetchProfileInfo() {
      const profileData = await this.$axios.$get(
        `profile/${this.$nuxt.context.params.id}/`
      )
      this.profile = profileData.results
      this.profileUser = profileData.results.profile[0]
    },
    async postComment() {
      if (!this.comment_input) {
        return
      }
      const form = new FormData()
      form.append('username', this.$auth.user.username)
      form.append('email', this.$auth.user.email)
      form.append('comment', this.comment_input)
      await this.$axios
        .$post(`feedback/${this.profileUser.id}/`, form)
        .then(async () => {
          await this.fetchProfileInfo()
          this.comment_input = ''
        })
    },
  },
}
</script>
