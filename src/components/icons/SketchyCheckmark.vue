<template>
  <div
    ref="checkmarkContainer"
    class="sketchy-checkmark"
  />
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import rough from 'roughjs'

const checkmarkContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  if (checkmarkContainer.value) {
    const rc = rough.svg(checkmarkContainer.value)
    const svg = rc.svg(`
    <svg width="20" height="20">
      ${
        rc.path('M4 10 L8 14 L16 6', {
          stroke: '#67c23a',
          strokeWidth: 2,
          roughness: 2,
          bowing: 2
        }).outerHTML
      }
    </svg>
  `)
    checkmarkContainer.value.innerHTML = ''
    checkmarkContainer.value.appendChild(svg)
  }
})
</script>

<style scoped>
.sketchy-checkmark {
  display: inline-block;
  width: 20px;
  height: 20px;
}
</style>
