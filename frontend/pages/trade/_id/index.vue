<template>
  <b-container v-if="!$fetchState.pending">
    <b-row>
      <b-col cols="4">
        <h4 class="mb-3">Items to trade</h4>
        <TradeItems :items="trade.have" class="mb-3" />
        <h4 class="mb-3">Items to recieve</h4>
        <TradeItems :items="trade.want" class="mb-3" />
      </b-col>
      <b-col cols="1"> </b-col>
      <b-col cols="7">
        <div class="d-flex flex-column">
          <div class="d-flex flex-row justify-content-between">
            <div class="d-flex flex-column">
              <h5 class="mb-3">
                Trade listed by
                <NuxtLink
                  :to="`/profile/${trade.creator.username}`"
                  class="link-collectr"
                  >{{ trade.creator.username }}</NuxtLink
                >
              </h5>
              <div
                v-if="trade.active"
                class="d-flex flex-row align-items-baseline mb-1"
              >
                <font-awesome-icon :icon="['fas', 'check']" />
                <h6 class="ml-2">{{ `This trade is active` }}</h6>
              </div>
              <div v-else class="d-flex flex-row align-items-baseline">
                <font-awesome-icon :icon="['fas', 'times']" />
                <h6 class="ml-2">{{ `This trade is closed` }}</h6>
              </div>
              <div
                v-if="trade.bookmarked"
                class="d-flex flex-row align-items-baseline"
              >
                <font-awesome-icon :icon="['fas', 'bookmark']" />
                <h6 class="ml-2">{{ `You bookmarked this trade` }}</h6>
              </div>
              <div v-else class="d-flex flex-row align-items-baseline">
                <font-awesome-icon :icon="['far', 'bookmark']" />
                <h6 class="ml-2">{{ `This trade is not bookmarked` }}</h6>
              </div>
            </div>
            <div class="d-flex flex-column">
              <b-button
                block
                variant="collectr-primary"
                @click="toggleBookmark"
              >
                {{ trade.bookmarked ? 'Remove bookmark' : 'Add bookmark' }}
              </b-button>
              <b-button
                v-if="trade.active && $auth.user.id === trade.creator.id"
                block
                variant="collectr-secondary"
                @click="closeTrade"
              >
                Close trade
                <font-awesome-icon
                  :icon="['fas', 'exclamation-triangle']"
                  class="ml-1"
                />
              </b-button>
            </div>
          </div>
          <p class="mt-2">
            <b>Description: </b>
            {{ trade.description }}
            <br />
            <b>Created on: </b>
            {{
              `${$moment(new Date(trade.creation_date)).format(
                'MMM Do YYYY'
              )} (${$moment(new Date(trade.creation_date)).fromNow()})`
            }}
          </p>
        </div>
        <h4 class="mb-3">Attachments</h4>
        <b-carousel
          v-if="trade.attachments.length"
          controls
          indicators
          no-touch
          :interval="0"
          class="mb-3"
        >
          <b-carousel-slide
            v-for="attachment in trade.attachments"
            :key="attachment.attachment"
            :img-src="attachment.attachment"
            img-height="400"
            :img-fluid="false"
          ></b-carousel-slide>
        </b-carousel>
        <p v-else class="mb-3">No attachments.</p>
        <h4 class="mb-3">Comments</h4>
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
        <Comment
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          class="mb-3"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      comment_input: '',
      trade: null,
      comments: [],
    }
  },
  async fetch() {
    await this.fetchTradeInfo()
    await this.fetchCommentInfo()
  },
  methods: {
    async fetchTradeInfo() {
      const response = await this.$axios.$get(
        `trades/${this.$nuxt.context.params.id}/`
      )
      this.trade = response
    },
    async fetchCommentInfo() {
      const response = await this.$axios.$get(
        `trades/${this.$nuxt.context.params.id}/comments/`
      )
      this.comments = response
    },
    async closeTrade() {
      const form = new FormData()
      form.append('active', false)
      await this.$axios
        .$patch(`trades/${this.trade.id}/`, form)
        .then(async () => {
          await this.fetchTradeInfo()
        })
    },
    async toggleBookmark() {
      await this.$axios
        .$post(`trades/${this.trade.id}/edit_bookmark/`)
        .then(async () => {
          await this.fetchTradeInfo()
        })
    },
    async postComment() {
      if (!this.comment_input) {
        return
      }
      const form = new FormData()
      form.append('trade', this.trade.id)
      form.append('username', this.$auth.user.username)
      form.append('email', this.$auth.user.email)
      form.append('comment', this.comment_input)
      await this.$axios
        .$post(`trades/${this.trade.id}/comments/`, form)
        .then(async () => {
          await this.fetchCommentInfo()
          this.comment_input = ''
        })
    },
  },
}
</script>

<style scoped>
.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
