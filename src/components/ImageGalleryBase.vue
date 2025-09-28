<template>
  <div class="image-gallery">
    <div class="gallery-grid">
      <div
        v-for="(img, index) in images"
        :key="index"
        class="image-item"
      >
        <wired-card elevation="2">
          <img
            :src="typeof img === 'string' ? img : img.url"
            :alt="typeof img === 'string' ? 'Image' : img.name"
            @click="$emit('image-click', img)"
          >
          <div class="image-actions">
            <slot
              name="actions"
              :image="img"
              :index="index"
            />
          </div>
        </wired-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  images: Array<string | {url: string; name: string; file: File}>
}>()

defineEmits<{
  (e: 'image-click', image: string | {url: string; name: string; file: File}): void
}>()
</script>

<style scoped>
.image-gallery {
  width: 100%;
  padding: 1rem;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.image-item {
  position: relative;
  aspect-ratio: 1;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  cursor: pointer;
}

.image-actions {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
}

:deep(wired-card) {
  height: 100%;

  --wired-card-background-color: transparent;
}
</style>
