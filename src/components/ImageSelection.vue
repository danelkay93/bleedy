<!-- ImageSelection.vue -->
<template>
  <div class="image-selection">
    <!-- Toolbar -->
    <div class="toolbar">
      <wired-button elevation="2" @click="openFilePicker">
        Browse
      </wired-button>

      <wired-search-input
        placeholder="Search Images..."
        v-model="searchQuery"
        class="search-input"
      ></wired-search-input>

      <div class="sort-select">
        <label for="sort">Sort By:</label>
        <wired-combo id="sort" v-model="sortOption" @change="sortFiles">
          <wired-item value="name">Name</wired-item>
          <wired-item value="date">Date Modified</wired-item>
          <wired-item value="size">Size</wired-item>
        </wired-combo>
      </div>
    </div>

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
      <div
        class="image-card"
        v-for="image in filteredFiles"
        :key="image.id"
        :class="{ 'selected-card': selectedImages.includes(image.id) }"
        @click="toggleSelection(image.id)"
      >
        <img :src="image.preview" :alt="image.name" class="image-thumbnail" />

        <div class="file-info">
          <div v-for="(value, key) in fileInfo(image)" :key="key">
            <small>
              {{ key }}:
              <span
                v-if="key === 'Filename' || key === 'Type'"
                v-html="highlightMatch(value, searchQuery)"
              ></span>
              <span v-else>{{ value }}</span>
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import 'wired-elements';

export default {
  components: {
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
    truncateText(text, maxLength) {
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    },
    fileInfo(image) {
      const { name, ext } = this.splitImageFilename(image.name);
      return {
        Filename: this.truncateText(name, 30),
        Type: ext,
        Modified: new Date(image.modifiedDate).toLocaleString(),
        Size: this.formatSize(image.size),
        Dimensions: image.dimensions || 'Loading...',
      };
    },
    highlightMatch(text, query) {
      if (!query) return text;
      const regex = new RegExp(`(${query})`, 'gi');
      return text.replace(regex, '<mark>$1</mark>');
    },
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
            const id = Date.now() + Math.random();
            const preview = URL.createObjectURL(file);
            const img = new Image();
            img.src = preview;
            img.onload = () => {
              const index = this.images.findIndex(image => image.id === id);
              if (index !== -1) {
                this.images[index].dimensions = `${img.width}x${img.height}`;
              }
            };
            return {
              id: Date.now() + Math.random(),
              name: file.name,
              preview: URL.createObjectURL(file),
              size: file.size,
              modifiedDate: file.lastModifiedDate || file.lastModified,
              dimensions: `${img.width}x${img.height}`,
            };
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

.toolbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input {
  width: 200px;
  background: transparent !important;
}

.sort-select {
  display: flex;
  align-items: center;
}

.sort-select label {
  margin-right: 0.5rem;
}

wired-combo {
  --wired-combo-popup-bg: var(--background-color, #fff);
  background: transparent;
}

wired-item {
  padding: 8px;
  background: transparent;
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

.image-card {
  width: 200px;
  border: 2px dashed #000;
  padding: 10px;
  cursor: pointer;
  background-color: #fff;
}

.image-card.selected-card {
  background-color: #ffd54f;
}

.image-thumbnail {
  width: 100%;
  height: auto;
  border: 1px solid #ccc;
}

.file-info {
  font-size: 12px;
  margin-top: 0.5rem;
}

mark {
  background-color: #ffff00;
  color: #000;
  padding: 0 2px;
  border-radius: 2px;
}
</style>
