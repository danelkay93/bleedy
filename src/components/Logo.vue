<template>
  <svg
    ref="svg"
    viewBox="0 0 100 120"
    width="100%"
    height="100%"
  />
</template>

<script lang="ts">
import {onMounted, ref} from 'vue'
import rough from 'roughjs/bundled/rough.esm.js'

export default {
  name: 'BloodLogo',
  setup() {
    const svg = ref(null)

    onMounted(() => {
      const rc = rough.svg(svg.value)

      const path = rc.path('M50,110 C20,110 0,90 50,10 C100,90 80,110 50,110 Z', {
        fill: 'red',
        stroke: 'black',
        strokeWidth: 2,
        fillStyle: 'hachure',
        fillWeight: 3,
        hachureGap: 8,
        hachureAngle: 60
      })

      svg.value.appendChild(path)
    })

    return {
      svg
    }
  }
}
</script>

<style scoped>
svg {
  display: block;
  margin: 0; /* Remove margins */
  padding: 0; /* Ensure no padding */
}
</style>
