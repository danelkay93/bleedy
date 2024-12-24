<template>
  <div class="review-results">
    <p>Review your processed images below:</p>
    <ImageGalleryBase :images="images">
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
</template>

<script setup lang="ts">
import { saveAs } from 'file-saver'
import JSZip from 'jszip'
import ImageGalleryBase from '../ImageGalleryBase.vue'

const props = defineProps<{
  images: string[]
}>()

async function downloadImage(imageUrl: string, index: number) {
  const response = await fetch(imageUrl)
  const blob = await response.blob()
  saveAs(blob, `processed-image-${index + 1}.${blob.type.split('/')[1]}`)
}

async function downloadZip() {
  const zip = new JSZip()
  
  // Add all images to zip
  await Promise.all(props.images.map(async (imageUrl, index) => {
    const response = await fetch(imageUrl)
    const blob = await response.blob()
    zip.file(
      `processed-image-${index + 1}.${blob.type.split('/')[1]}`,
      blob
    )
  }))
  
  // Generate and download zip
  const content = await zip.generateAsync({ type: 'blob' })
  saveAs(content, 'processed-images.zip')
}
</script>

<style scoped>
.review-results {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.download-all {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
</style>
