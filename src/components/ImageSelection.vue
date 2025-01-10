<!-- ImageSelection.vue -->
<template>
  <el-row justify="center">
    <el-col :span="20">
      <div class="image-selection">
        <SearchToolbar v-model:searchQuery="searchQuery" @browse="openFilePicker" />

        <!-- Status Messages -->
        <div v-if="activeStep === 0" class="status-messages">
          <div v-if="images.length === 0" class="no-images">
            <p>No images selected.</p>
            <p>Click the "Browse" button to select images.</p>
          </div>
          <div v-else>
            <p v-if="filteredFiles.length === 0">No images match the current search filter.</p>
            <p v-else class="selection-counter">
              {{
                searchQuery.trim()
                  ? `${filteredFiles.length}/${images.length} images displayed`
                  : `${selectedImages.length}/${images.length} images selected`
              }}
            </p>
          </div>
        </div>

        <!-- Image Grid -->
        <div v-if="activeStep === 0 && filteredFiles.length > 0" class="image-grid">
          <ImageGalleryItem
            v-for="image in filteredFiles"
            :key="image.id"
            :image="image"
            :selected="selectedImages.includes(image.id)"
            :searchQuery="searchQuery"
            @remove="removeImage(image.id)" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import { ref, computed } from 'vue'
import 'wired-elements'

export default {
  components: {
    ImageGalleryItem: () => import('./ImageGalleryItem.vue'),
    SearchToolbar: () => import('./SearchToolbar.vue')
  },
  props: {
    activeStep: Number
  },
  emits: ['update:selectedImages'],
  data() {
    return {
      selectedImages: [],
      images: [],
      searchQuery: '',
      sortOption: 'name' // default sort option
    }
  },
  computed: {
    filteredFiles() {
      let images = [...this.images]

      // Search filter
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase().trim()
        images = images.filter(
          (file) =>
            file.name.toLowerCase().includes(query) ||
            this.splitImageFilename(file.name).ext.toLowerCase().includes(query)
        )
      }

      // Sorting
      if (this.sortOption === 'name') {
        images = images.sort((a, b) => a.name.localeCompare(b.name))
      } else if (this.sortOption === 'date') {
        images = images.sort((a, b) => new Date(b.modifiedDate) - new Date(a.modifiedDate))
      } else if (this.sortOption === 'size') {
        images = images.sort((a, b) => b.size - a.size)
      }

      return images
    }
  },
  methods: {
    removeImage(imageId) {
      // Remove from selected images
      const selectedIndex = this.selectedImages.indexOf(imageId)
      if (selectedIndex > -1) {
        this.selectedImages.splice(selectedIndex, 1)
      }

      // Remove from images array and revoke URL
      const imageIndex = this.images.findIndex((img) => img.id === imageId)
      if (imageIndex > -1) {
        const image = this.images[imageIndex]
        if (image.preview) {
          URL.revokeObjectURL(image.preview)
        }
        this.images.splice(imageIndex, 1)
      }

      this.$emit('update:selectedImages', this.selectedImages)
    },
    openFilePicker() {
      const options = {
        types: [
          {
            description: 'Image Files',
            accept: {
              'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp']
            }
          }
        ],
        multiple: true
      }
      window
        .showOpenFilePicker(options)
        .then((fileHandles) => Promise.all(fileHandles.map((handle) => handle.getFile())))
        .then((files) => {
          const newImages = files.map((file) => {
            const imageId = Date.now() + Math.random()
            const preview = URL.createObjectURL(file)
            return {
              id: imageId,
              name: file.name,
              preview,
              size: file.size,
              modifiedDate: file.lastModifiedDate || file.lastModified,
              dimensions: 'Loading...',
              file // Keep reference to original file
            }
          })

          // Add new images and their IDs to selected images
          this.images = [...this.images, ...newImages]
          const newSelectedImages = [...this.selectedImages, ...newImages.map((img) => img.id)]
          this.selectedImages = newSelectedImages
          this.$emit(
            'update:selectedImages',
            newSelectedImages.map((id) => this.images.find((img) => img.id === id).file)
          )
        })
        .then(() => {
          // Load dimensions for each image after they're added
          this.images.forEach((imageData) => {
            const img = new Image()
            img.onload = () => {
              const index = this.images.findIndex((i) => i.id === imageData.id)
              if (index !== -1) {
                this.images[index].dimensions = `${img.naturalWidth}x${img.naturalHeight}`
              }
            }
            img.src = imageData.preview
          })
        })
        .catch((err) => console.error('Error selecting files:', err))
    },
    sortFiles() {
      // Sorting is handled in the computed property `filteredFiles`
    },
    formatSize(size) {
      const i = Math.floor(Math.log(size) / Math.log(1024))
      return (size / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i]
    },
    splitImageFilename(filename) {
      const lastDotIndex = filename.lastIndexOf('.')
      if (lastDotIndex === -1) return { name: filename, ext: '' }
      const name = filename.slice(0, lastDotIndex)
      const ext = filename.slice(lastDotIndex + 1)
      return { name: name, ext: ext }
    }
  },
  beforeUnmount() {
    // Clean up object URLs
    this.images.forEach((image) => {
      if (image.preview) {
        URL.revokeObjectURL(image.preview)
      }
    })
  }
}
</script>

<style scoped>
@import '../../node_modules/doodle.css/doodle.css';
@import '../assets/handdrawn.css';
@import '../../node_modules/paper-css/paper.css';

.image-selection {
  width: 100%;
}

.status-messages {
  text-align: center;
  font-family: 'Doodle', sans-serif;
  margin: 1rem 0;
}

.no-images {
  margin: 1rem 0;
}

.selection-counter {
  font-weight: bold;
  color: #666;
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}
</style>
