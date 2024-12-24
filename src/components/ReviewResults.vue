<template>
  <div class="review-results">
    <h3>Review Processed Images</h3>
    <el-scrollbar class="image-scrollbar">
      <div v-if="images.length > 0" class="image-grid">
        <el-card v-for="(image, index) in images" :key="index" class="image-card" shadow="hover">
          <el-image :src="image" fit="contain" :preview-src-list="[image]" />
        </el-card>
      </div>
      <p v-else class="no-images">No processed images available.</p>
    </el-scrollbar>
    <el-button v-if="images.length > 0" type="primary" @click="handleSaveZip" :loading="isSaving">
      {{ isSaving ? 'Saving...' : 'Save All as ZIP' }}
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  onSaveZip: {
    type: Function,
    required: true
  }
})

const isSaving = ref(false)

async function handleSaveZip() {
  isSaving.value = true
  try {
    await props.onSaveZip()
  } catch (error) {
    console.error('Error saving ZIP:', error)
    // You might want to show an error message to the user here
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
.review-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.image-scrollbar {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.image-card {
  width: 100%;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.no-images {
  text-align: center;
  color: #909399;
}

.el-button {
  margin-top: 20px;
}
</style>