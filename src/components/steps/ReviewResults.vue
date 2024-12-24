<template>
  <div>
    <p>Review your processed images below:</p>
    <div class="image-gallery">
      <img
        v-for="(img, index) in images"
        :key="index"
        :src="img"
        alt="Processed Image" 
      />
    </div>
    <wired-button @click="$emit('save')">Save as ZIP</wired-button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  images: string[]
}>()

defineEmits<{
  (e: 'save'): void
}>()
</script>

<style scoped>
.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-gallery img {
  max-width: 100%;
  height: auto;
  border: 2px dashed #000;
}
</style>
