<template>
  <div class="process-and-review">
    <div class="process-header">
      <h3>Ready to add bleed to {{ imageCount }} images</h3>
      <p>Using {{ bleedAmount }}px bleed margin</p>
    </div>
    <!-- <div id="bleedy-output" class="output-container"></div> Removed this -->
    <div
      class="process-status"
      v-if="processing || (totalFiles > 0 && processedCount < totalFiles)">
      <ImageProcessingProgress
        :progress="progress"
        :processed-count="processedCount"
        :total-files="totalFiles"
        :elapsed-time="elapsedTime"
        :remaining-time="remainingTime" />
    </div>
    <div class="process-actions">
      <wired-button @click="handleProcess" :disabled="processing && processedCount < totalFiles">
        {{
          processing && processedCount < totalFiles
            ? 'Processing...'
            : processedCount === totalFiles && totalFiles > 0
              ? 'Done!'
              : 'Add Bleed!'
        }}
      </wired-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, onMounted, onUnmounted} from 'vue'
import ImageProcessingProgress from '../ImageProcessingProgress.vue'

const props = defineProps<{
  images: File[] // Expect an array of File objects
  bleedAmount: number
}>()

const emit = defineEmits<{
  (e: 'process-complete', images: string[]): void
}>()

const processing = ref(false) // True when the process is initiated and not yet fully completed or timed out
const progress = ref(0)
const processedCount = ref(0)
const totalFiles = ref(0) // Will be set from props.images.length or progress event
const elapsedTime = ref(0)
const remainingTime = ref(0)

const tempProcessedImages = ref<string[]>([]) // Temporarily collects blob URLs as they arrive
const finalProcessedImages = ref<string[]>([]) // Stores the final list for emit once all are done

interface ProgressEventDetail {
  progress: number
  processed: number
  total: number
  elapsed: number
  remaining: number
}

interface PyScriptProgressEvent extends CustomEvent {
  detail: ProgressEventDetail
}

function handleProgressEvent(event: PyScriptProgressEvent) {
  // console.log('JS: Progress event received', event.detail);
  const {detail} = event
  progress.value = detail.progress
  processedCount.value = detail.processed
  totalFiles.value = detail.total // Update totalFiles from the event if Python calculates it
  elapsedTime.value = detail.elapsed
  remainingTime.value = detail.remaining

  // If all files reported by progress event are processed, but not yet by individual image events
}

interface ProcessedImageEventDetail {
  name: string
  blobUrl: string
  format: string
}
interface BleedyImageProcessedEvent extends CustomEvent {
  detail: ProcessedImageEventDetail
}

function handleProcessedImageEvent(event: BleedyImageProcessedEvent) {
  console.log('JS: Received processed image event', event.detail)
  tempProcessedImages.value.push(event.detail.blobUrl)

  // Check if all images are processed
  // totalFiles should be reliable from the first progress event or props.images.length
  if (totalFiles.value > 0 && tempProcessedImages.value.length === totalFiles.value) {
    console.log('✨ JS: All images processed and ready (via individual events)')
    finalProcessedImages.value = [...tempProcessedImages.value]
    emit('process-complete', finalProcessedImages.value)
    processing.value = false // Indicate processing is no longer active

    // It's crucial to clean up this specific listener once all expected images are received.
    window.removeEventListener('bleedy-image-processed', handleProcessedImageEvent as EventListener)
  }
}

let processTimeoutId: number | null = null

onMounted(() => {
  window.addEventListener('processing-progress', handleProgressEvent as EventListener)
  // The 'bleedy-image-processed' listener is added dynamically in handleProcess
})

onUnmounted(() => {
  window.removeEventListener('processing-progress', handleProgressEvent as EventListener)
  window.removeEventListener('bleedy-image-processed', handleProcessedImageEvent as EventListener) // Ensure cleanup on unmount
  if (processTimeoutId) {
    clearTimeout(processTimeoutId)
  }
})

const imageCount = computed(() => props.images.length)

async function handleProcess() {
  if (props.images.length === 0) {
    console.warn('JS: No images to process.')
    return
  }

  console.log('JS: handleProcess initiated')
  processing.value = true
  progress.value = 0
  processedCount.value = 0
  totalFiles.value = props.images.length // Set totalFiles from props
  elapsedTime.value = 0
  remainingTime.value = 0
  tempProcessedImages.value = []
  finalProcessedImages.value = []

  // Add listener for individual processed images for this processing session
  window.addEventListener('bleedy-image-processed', handleProcessedImageEvent as EventListener)

  try {
    const event = new CustomEvent('process-images', {
      detail: {
        files: props.images, // Pass the array of File objects
        bleedAmount: props.bleedAmount
      }
    })

    const processorElement = document.querySelector('.image-bleed-processor')
    if (processorElement) {
      console.log("JS: Dispatching 'process-images' event to PyScript", event.detail)
      processorElement.dispatchEvent(event)
    } else {
      console.error('JS: Could not find .image-bleed-processor element to dispatch event.')
      processing.value = false
      window.removeEventListener(
        'bleedy-image-processed',
        handleProcessedImageEvent as EventListener
      )
      return
    }

    // Timeout for the entire process
    const TIMEOUT_PER_IMAGE_MS = 60000 // 1 minute per image
    processTimeoutId = setTimeout(() => {
      if (processing.value && tempProcessedImages.value.length !== totalFiles.value) {
        console.error(
          'JS: Processing timeout: Not all images were processed within the expected time.'
        )
        processing.value = false // Stop processing indicator
        window.removeEventListener(
          'bleedy-image-processed',
          handleProcessedImageEvent as EventListener
        ) // Cleanup
        // Here you might want to emit a partial result or an error state to the parent
        if (tempProcessedImages.value.length > 0) {
          emit('process-complete', [...tempProcessedImages.value]) // Emit whatever was processed
        }
        // Optionally, show an error to the user
      }
const timeoutId = window.setTimeout(
  () => { /* … */ },
  TIMEOUT_PER_IMAGE_MS * totalFiles.value
)
  } catch (error) {
    console.error('JS: Error dispatching process-images event:', error)
    processing.value = false
    window.removeEventListener('bleedy-image-processed', handleProcessedImageEvent as EventListener)
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

/* .output-container style removed as element is gone */

.process-status {
  width: 100%;
  max-width: 400px; /* Or adjust as needed */
  margin: 1rem auto; /* Centering if max-width is applied */
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
  text-align: center; /* Center the button */
}

:deep(wired-button[disabled]) {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
