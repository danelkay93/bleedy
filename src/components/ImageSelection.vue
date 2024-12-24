<!-- ImageSelection.vue -->
<template>
  <div class="image-selection">
    <SearchToolbar
      v-model:searchQuery="searchQuery"
      v-model:sortOption="sortOption"
      @browse="openFilePicker"
    />

    <!-- No Images Selected -->
    <div v-if="activeStep === 0 && filteredFiles.length === 0" class="no-images">
      <p>No images selected.</p>
      <p>Click the "Browse" button to select images.</p>
    </div>

    <!-- Image Grid -->
    <div
      v-if="activeStep === 0 && filteredFiles.length > 0"
      class="image-grid"
    >
      <ImageGalleryItem
        v-for="image in filteredFiles"
        :key="image.id"
        :image="image"
        :selected="selectedImages.includes(image.id)"
        :searchQuery="searchQuery"
        @toggle="toggleSelection(image.id)"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import 'wired-elements';

export default {
  components: {
    ImageGalleryItem: () => import('./ImageGalleryItem.vue'),
    SearchToolbar: () => import('./SearchToolbar.vue'),
  },
  props: {
    activeStep: Number,
  },
  emits: ['update:selectedImages'],
  data() {
    return {
      selectedImages: [],
      images: [],
      searchQuery: '',
      sortOption: 'name', // default sort option
    };
  },
  computed: {
    filteredFiles() {
      let images = [...this.images];

      // Search filter
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase().trim();
        images = images.filter((file) => 
          file.name.toLowerCase().includes(query) ||
          this.splitImageFilename(file.name).ext.toLowerCase().includes(query)
        );
      }

      // Sorting
      if (this.sortOption === 'name') {
        images = images.sort((a, b) => a.name.localeCompare(b.name));
      } else if (this.sortOption === 'date') {
        images = images.sort((a, b) => new Date(b.modifiedDate) - new Date(a.modifiedDate));
      } else if (this.sortOption === 'size') {
        images = images.sort((a, b) => b.size - a.size);
      }

      return images;
    },
  },
  methods: {
    toggleSelection(imageId) {
      const index = this.selectedImages.indexOf(imageId);
      if (index > -1) {
        this.selectedImages.splice(index, 1);
      } else {
        this.selectedImages.push(imageId);
      }
      this.$emit('update:selectedImages', this.selectedImages);
    },
    openFilePicker() {
      const options = {
        types: [
          {
            description: 'Image Files',
            accept: {
              'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
            },
          },
        ],
        multiple: true,
      };
      window
        .showOpenFilePicker(options)
        .then((fileHandles) => Promise.all(fileHandles.map((handle) => handle.getFile())))
        .then((files) => {
          this.images = files.map((file) => {
            const imageId = Date.now() + Math.random();
            const preview = URL.createObjectURL(file);
            return {
              id: imageId,
              name: file.name,
              preview,
              size: file.size,
              modifiedDate: file.lastModifiedDate || file.lastModified,
              dimensions: 'Loading...',
              file // Keep reference to original file
            };
          });
        })
        .then(() => {
          // Load dimensions for each image after they're added
          this.images.forEach(imageData => {
            const img = new Image();
            img.onload = () => {
              const index = this.images.findIndex(i => i.id === imageData.id);
              if (index !== -1) {
                this.images[index].dimensions = `${img.naturalWidth}x${img.naturalHeight}`;
              }
              URL.revokeObjectURL(imageData.preview); // Clean up the URL
            };
            img.src = imageData.preview;
          });
        })
        .catch((err) => console.error('Error selecting files:', err));
    },
    sortFiles() {
      // Sorting is handled in the computed property `filteredFiles`
    },
    formatSize(size) {
      const i = Math.floor(Math.log(size) / Math.log(1024));
      return (size / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
    },
    splitImageFilename(filename) {
      const lastDotIndex = filename.lastIndexOf('.');
      if (lastDotIndex === -1) return { name: filename, ext: '' };
      const name = filename.slice(0, lastDotIndex);
      const ext = filename.slice(lastDotIndex + 1);
      return { name: name, ext: ext };
    },
  },
};
</script>

<style scoped>
@import '../../node_modules/doodle.css/doodle.css';
@import '../assets/handdrawn.css';
@import 'papercss/dist/paper.min.css';

.image-selection {
  width: 100%;
}


.no-images {
  text-align: center;
  font-family: 'Doodle', sans-serif;
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

</style>
