<template>
  <div class="process-images">
    <div class="process-header">
      <h3>Ready to add bleed to {{ imageCount }} images</h3>
      <p>Using {{ bleedAmount }}px bleed margin</p>
    </div>
    <div id="bleedy-output" class="output-container"></div>
    <div class="process-actions">
      <wired-button @click="handleProcess" :disabled="processing">
        {{ processing ? 'Processing...' : 'Process Images' }}
      </wired-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  images: File[]
  bleedAmount: number
}>()

const processing = ref(false)

const imageCount = computed(() => props.images.length)

const emit = defineEmits<{
  (e: 'process-complete', processedImages: string[]): void
}>()

async function handleProcess() {
  processing.value = true
  
  // Create custom event for PyScript
  const event = new CustomEvent('process-images', {
    detail: {
      files: props.images,
      bleedAmount: props.bleedAmount
    }
  })
  
  document.querySelector('div[class="image-processor-wrapper"]')?.dispatchEvent(event)
  
  // Wait for PyScript to process images
  // TODO: Implement proper completion detection
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  processing.value = false
  
  // Get processed images from output container
  const processedImages = Array.from(
    document.getElementById('bleedy-output')?.getElementsByTagName('img') || []
  ).map(img => img.src)
  
  emit('process-complete', processedImages)
}
</script>

<style scoped>
.process-images {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.process-header {
  text-align: center;
}

.output-container {
  display: none;
}

.process-actions {
  margin-top: 1rem;
}

:deep(wired-button[disabled]) {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
