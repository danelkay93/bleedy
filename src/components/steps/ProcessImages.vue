<template>
  <div class="process-and-review">
    <div v-if="!processedImages.length" class="process-section">
      <div class="process-header">
        <h3>Ready to add bleed to {{ imageCount }} images</h3>
        <p>Using {{ bleedAmount }}px bleed margin</p>
      </div>
      <div id="bleedy-output" class="output-container"></div>
      <div class="process-actions">
        <wired-button @click="handleProcess" :disabled="processing">
          {{ processing ? 'Processing...' : 'Add Bleed!' }}
        </wired-button>
      </div>
    </div>

    <div v-else class="review-section">
      <p>Review your processed images below:</p>
      <ImageGalleryBase :images="processedImages">
        <template #actions="{ image, index }">
          <wired-button @click="downloadImage(image, index)">
            Download
          </wired-button>
        </template>
      </ImageGalleryBase>
      <div class="download-all">
        <wired-button @click="downloadZip">Download All as ZIP</wired-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { saveAs } from 'file-saver'
import JSZip from 'jszip'
import ImageGalleryBase from '../ImageGalleryBase.vue'

const props = defineProps<{
  images: File[]
  bleedAmount: number
}>()

const emit = defineEmits<{
  (e: 'process-complete', images: string[]): void
}>()

const processing = ref(false)
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
    
    document.querySelector('.process-and-review')?.dispatchEvent(event)
    
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
        const imageUrls = images.map(img => img.src)
        processedImages.value = imageUrls
        emit('process-complete', imageUrls)
        break
      }
      await new Promise(resolve => setTimeout(resolve, checkInterval))
      waitTime += checkInterval
    }

    if (waitTime >= maxWaitTime) {
      throw new Error('Timeout waiting for images to process')
    }
    
    // Get processed images from output container
    const images = Array.from(
      document.getElementById('bleedy-output')?.getElementsByTagName('img') || []
    ).map(img => img.src)
    
    processedImages.value = images
    emit('process-complete', images)
  } catch (error) {
    console.error('Error processing images:', error)
  } finally {
    processing.value = false
  }
}

async function downloadImage(imageUrl: string, index: number) {
  const response = await fetch(imageUrl)
  const blob = await response.blob()
  saveAs(blob, `processed-image-${index + 1}.${blob.type.split('/')[1]}`)
}

async function downloadZip() {
  const zip = new JSZip()
  
  await Promise.all(processedImages.value.map(async (imageUrl, index) => {
    const response = await fetch(imageUrl)
    const blob = await response.blob()
    zip.file(
      `processed-image-${index + 1}.${blob.type.split('/')[1]}`,
      blob
    )
  }))
  
  const content = await zip.generateAsync({ type: 'blob' })
  saveAs(content, 'processed-images.zip')
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

.process-actions,
.download-all {
  margin-top: 1rem;
}

:deep(wired-button[disabled]) {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
