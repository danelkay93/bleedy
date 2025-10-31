<template>
  <div class="process-and-review">
    <div class="process-header">
      <h3>Ready to add bleed to {{ imageCount }} images</h3>
      <p>Using {{ bleedAmount }}px bleed margin</p>
    </div>
    <div id="bleedy-output" class="output-container"></div>
    <div class="process-status" v-if="processing">
      <ImageProcessingProgress
        :progress="progress"
        :processed-count="processedCount"
        :total-files="totalFiles"
        :elapsed-time="elapsedTime"
        :remaining-time="remainingTime" />
    </div>
    <div class="process-actions">
      <wired-button @click="handleProcess" :disabled="processing">
        {{ processing ? 'Processing...' : 'Add Bleed!' }}
      </wired-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ImageProcessingProgress from '../ImageProcessingProgress.vue'

const props = defineProps<{
  images: File[]
  bleedAmount: number
}>()

const emit = defineEmits<{
  (e: 'process-complete', images: string[]): void
}>()

const processing = ref(false)
const progress = ref(0)
const processedCount = ref(0)
const totalFiles = ref(0)
const elapsedTime = ref(0)
const remainingTime = ref(0)

interface ProgressEvent extends CustomEvent {
  detail: {
    progress: number
    processed: number
    total: number
    elapsed: number
    remaining: number
  }
}

function handleProgressEvent(event: ProgressEvent) {
  const { detail } = event
  progress.value = detail.progress
  processedCount.value = detail.processed
  totalFiles.value = detail.total
  elapsedTime.value = detail.elapsed
  remainingTime.value = detail.remaining
}

onMounted(() => {
  window.addEventListener('processing-progress', handleProgressEvent as EventListener)
})

onUnmounted(() => {
  window.removeEventListener('processing-progress', handleProgressEvent as EventListener)
})
const processedImages = ref<string[]>([])
const imageCount = computed(() => props.images.length)

async function handleProcess() {
  processing.value = true

  try {
    // Create custom event for PyScript
    const event = new CustomEvent('process-images', {
      detail: {
        files: props.images,
        bleedAmount: props.bleedAmount
      }
    })

    document.querySelector('.image-bleed-processor')?.dispatchEvent(event)

    // Wait for PyScript to process images
    const maxWaitTime = 10000 // 10 seconds
    const checkInterval = 100 // 100ms
    let waitTime = 0

    while (waitTime < maxWaitTime) {
      const images = Array.from(
        document.getElementById('bleedy-output')?.getElementsByTagName('img') || []
      )
      if (images.length === props.images.length) {
        console.log('✨ All images processed and ready')
        const imageUrls = images.map((img) => img.src)
        processedImages.value = imageUrls
        emit('process-complete', imageUrls)
        break
      }
      await new Promise((resolve) => setTimeout(resolve, checkInterval))
      waitTime += checkInterval
    }

    if (waitTime >= maxWaitTime) {
      throw new Error('Timeout waiting for images to process')
    }

    // Get processed images from output container
    const images = Array.from(
      document.getElementById('bleedy-output')?.getElementsByTagName('img') || []
    ).map((img) => img.src)

    processedImages.value = images
    emit('process-complete', images)
  } catch (error) {
    console.error('Error processing images:', error)
  } finally {
    processing.value = false
  }
}
</script>

<style scoped>
.process-and-review {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.process-section,
.review-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.process-header {
  text-align: center;
}

.output-container {
  position: absolute;
  left: -9999px;
}

.process-status {
  width: 100%;
  max-width: 400px;
  margin: 1rem 0;
}

.status-text {
  font-family: 'Architects Daughter', cursive;
  text-align: center;
  margin-top: 0.5rem;
}

.status-text p {
  margin: 0.25rem 0;
}

.process-actions,
.download-all {
  margin-top: 1rem;
}

:deep(wired-button[disabled]) {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
