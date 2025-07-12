<template>
  <div
    class="image-card"
    :class="{'selected-card': selected}"
  >
    <img
      :src="image.preview"
      :alt="image.name"
      :title="image.name"
      class="image-thumbnail"
    >

    <div class="file-info">
      <div
        v-for="(value, key) in fileInfo"
        :key="key"
      >
        <small>
          {{ key }}:
          <span
            v-if="key === 'Filename' || key === 'Type'"
            v-html="highlightMatch(value, searchQuery)"
          />
          <span v-else>{{ value }}</span>
        </small>
      </div>
    </div>
    <wired-button
      v-if="selected"
      class="remove-button"
      elevation="2"
      @click.stop="$emit('remove')"
    >
      ✕
    </wired-button>
  </div>
</template>

<script lang="ts">
export default {
  name: 'ImageGalleryItem',
  props: {
    image: {
      type: Object,
      required: true
    },
    selected: {
      type: Boolean,
      default: false
    },
    searchQuery: {
      type: String,
      default: ''
    }
  },
  emits: ['remove'],
  computed: {
    fileInfo() {
      const {name, ext} = this.splitImageFilename(this.image.name)
      return {
        Filename: this.truncateText(name, 30),
        Type: ext,
        Modified: new Date(this.image.modifiedDate).toLocaleString(),
        Size: this.formatSize(this.image.size),
        Dimensions: this.image.dimensions || 'Loading...'
      }
    }
  },
  methods: {
    truncateText(text: string, maxLength: number) {
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    },
    highlightMatch(text: string, query: string) {
      if (!query) return text
      const regex = new RegExp(`(${query})`, 'gi')
      return text.replace(regex, '<mark>$1</mark>')
    },
    formatSize(size: number) {
      const i = Math.floor(Math.log(size) / Math.log(1024))
      return (size / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i]
    },
    splitImageFilename(filename: string) {
      const lastDotIndex = filename.lastIndexOf('.')
      if (lastDotIndex === -1) return {name: filename, ext: ''}
      const name = filename.slice(0, lastDotIndex)
      const ext = filename.slice(lastDotIndex + 1)
      return {name: name, ext: ext}
    }
  }
}
</script>

<style scoped>
.image-card {
  width: 200px;
  border: 2px dashed #000;
  padding: 10px;
  background-color: #fff;
  position: relative;
  display: flex;
  flex-direction: column;
}

.remove-button {
  position: absolute;
  bottom: 10px;
  right: 10px;
  --wired-button-background-color: #ff4444;
  --wired-button-color: white;
  font-size: 12px;
  padding: 2px;
  min-width: 24px;
  min-height: 24px;
  z-index: 1;
}

.remove-button:hover {
  --wired-button-background-color: #ff0000;
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
