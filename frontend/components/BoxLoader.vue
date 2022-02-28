<template>
  <b-img src="/img/collectr-box.svg" class="rotate" :style="styles"></b-img>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      default: '50px',
    },
    background: {
      type: String,
      default: 'white',
    },
  },
  computed: {
    styles() {
      return {
        width: this.size,
        height: this.size,
        backgroundColor: this.background,
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.rotate {
  animation: rotation 1.5s infinite linear;
}

@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}
</style>
