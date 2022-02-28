<template>
  <b-row class="comment p-1">
    <b-col>
      <b-row class="pt-1 pb-2">
        <b-col cols="6">{{ `${comment.username} | ${comment.email}` }} </b-col>
        <b-col cols="6" style="text-align: right">
          {{ new Date(comment.timestamp).toLocaleDateString('en-US') }}</b-col
        >
      </b-row>
      <b-row class="pb-1">
        <b-col> {{ comment.comment }}</b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    comment: {
      type: Object,
      default: () => {},
    },
  },
}
</script>

<style>
.comment {
  background-color: #f2f2f2;
  border-radius: 10px;
}
</style>
