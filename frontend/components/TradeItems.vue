// literally so cursed. there has to be a better way to do this...

<template>
  <b-row>
    <b-col>
      <b-row>
        <b-col
          v-for="(n, i) in 3"
          :key="i"
          cols="4"
          :class="{ 'p-0': inListing }"
          align-v="center"
        >
          <NuxtLink
            v-if="!inListing && itemAt(i).id != null"
            :to="`/item/${itemAt(i).id}`"
            class="link-invisible"
          >
            <b-img
              thumbnail
              fluid
              :src="itemAt(i).cover_image"
              :class="{ 'mb-3': !inListing }"
            ></b-img>
          </NuxtLink>
          <b-img
            v-else
            thumbnail
            fluid
            :src="itemAt(i).cover_image"
            :class="{ 'mb-3': !inListing }"
          ></b-img>
        </b-col>
      </b-row>
      <b-row>
        <b-col
          v-for="(n, i) in 3"
          :key="i"
          cols="4"
          :class="{ 'p-0': inListing }"
          align-v="center"
        >
          <NuxtLink
            v-if="!inListing && itemAt(i + 3).id != null"
            :to="`/item/${itemAt(i).id}`"
            class="link-invisible"
          >
            <b-img
              thumbnail
              fluid
              :src="itemAt(i + 3).cover_image"
              :class="{ 'mb-3': !inListing }"
            ></b-img>
          </NuxtLink>
          <b-img
            v-else
            thumbnail
            fluid
            :src="itemAt(i + 3).cover_image"
            :class="{ 'mb-3': !inListing }"
          ></b-img>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      default: () => {},
    },
    inListing: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      defaultItem: {
        id: null,
        cover_image: 'https://dummyimage.com/500x500/f2f2f2/ffffff.png&text=+',
      },
    }
  },
  computed: {
    renderLink(index) {
      return this.items.length > index
    },
  },
  methods: {
    itemAt(index) {
      if (this.items.length > index) {
        return this.items[index]
      }
      return this.defaultItem
    },
  },
}
</script>
