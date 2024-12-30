<template>
  <div class="wired-progress">
    <div class="progress-bar" ref="progressBar"></div>
    <div class="progress-text">
      {{ Math.round(progress) }}%
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import rough from 'roughjs'

const props = defineProps<{
  progress: number
}>()

const progressBar = ref<HTMLElement>()

function drawProgress() {
  if (!progressBar.value) return
  
  const width = progressBar.value.offsetWidth
  const height = progressBar.value.offsetHeight
  
  // Clear previous content
  progressBar.value.innerHTML = ''
  
  const rc = rough.svg(width, height)
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svg.setAttribute('width', width.toString())
  svg.setAttribute('height', height.toString())
  
  // Draw outer rectangle
  const outer = rc.rectangle(0, 0, width, height, {
    stroke: '#000',
    strokeWidth: 1,
    fill: 'none',
    fillStyle: 'solid'
  })
  svg.appendChild(outer)
  
  // Draw progress fill
  const fillWidth = (width * props.progress) / 100
  if (fillWidth > 0) {
    const fill = rc.rectangle(0, 0, fillWidth, height, {
      stroke: 'none',
      fill: '#000',
      fillStyle: 'zigzag'
    })
    svg.appendChild(fill)
  }
  
  progressBar.value.appendChild(svg)
}

onMounted(drawProgress)
watch(() => props.progress, drawProgress)
</script>

<style scoped>
.wired-progress {
  position: relative;
  width: 100%;
  height: 20px;
  margin: 10px 0;
}

.progress-bar {
  width: 100%;
  height: 100%;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-family: 'Architects Daughter', cursive;
  font-size: 0.9em;
}
</style>
