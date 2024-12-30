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
import { useImageDownload } from '../../composables/useImageDownload'
import ImageGalleryBase from '../ImageGalleryBase.vue'

const props = defineProps<{
  images: string[]
}>()

const { downloadImage, downloadZip } = useImageDownload()

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
