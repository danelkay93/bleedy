<template>
  <div class="image-gallery">
    <!-- Search bar -->
    <input
      v-model="searchQuery"
      placeholder="Search images..."
      class="search-bar"
    >

    <!-- File picker button -->
    <el-button @click="openFilePicker">
      Select Images
    </el-button>

    <!-- Draggable image thumbnails -->
    <draggable
      v-model="filteredImages"
      class="image-list"
      @end="onEnd"
    >
      <template #item="{element}">
        <div class="image-item">
          <img
            :src="element.url"
            alt="image"
            @click="openLightbox(element.url)"
          >
          <el-button
            type="danger"
            @click="removeImage(element)"
          >
            Remove
          </el-button>
        </div>
      </template>
    </draggable>

    <!-- Lightbox component for image preview -->
    <vue-preview
      ref="lightbox"
      :images="lightboxImages"
    />
  </div>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue'
import draggable from 'vuedraggable'
import {VuePreview} from 'vue3-image-preview'

type GalleryImage = {
  url: string
  name: string
  file: File
}

const images = ref<GalleryImage[]>([]) // All images
const searchQuery = ref('') // For searching images
const lightboxImages = ref<string[]>([]) // Lightbox images for preview
const lightbox = ref<InstanceType<typeof VuePreview> | null>(null)

// Filtered images based on search
const filteredImages = computed(() => {
  if (!searchQuery.value) return images.value
  return images.value.filter((img) =>
    img.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Function to open file picker using File System API
async function openFilePicker() {
  try {
    const fileHandles = await window.showOpenFilePicker({
      multiple: true,
      types: [{description: 'Images', accept: {'image/*': ['.png', '.jpg', '.jpeg']}}]
    })

    // Convert FileHandles to file URLs and push to the images array
    const selectedImages = await Promise.all(
      fileHandles.map(async (fileHandle) => {
        const file = await fileHandle.getFile()
        return {
          url: URL.createObjectURL(file),
          name: file.name,
          file
        }
      })
    )
    images.value.push(...selectedImages)
  } catch (error) {
    console.error('Error selecting images:', error)
  }
}

// Remove image from the gallery
function removeImage(image: GalleryImage) {
  images.value = images.value.filter((img) => img !== image)
}

// Open image in lightbox
function openLightbox(url: string) {
  lightboxImages.value = [url] // Display the clicked image
  lightbox.value?.show()
}

// Sort end event handler
function onEnd() {
  console.log('Sorted images:', images.value)
}
</script>

<style scoped>
.image-gallery {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.search-bar {
  margin-bottom: 20px;
  padding: 10px;
  width: 300px;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.image-item {
  position: relative;
  display: inline-block;
}

.image-item img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  cursor: pointer;
  border-radius: 8px;
}

.el-button {
  margin-top: 10px;
}
</style>
