<template>
  <div class="process-images">
    <h3>Process Images</h3>
    <p>Click the button below to start processing your images with the selected bleed settings.</p>
    <el-button @click="handleProcessImages" type="primary" :loading="isProcessing">
      {{ isProcessing ? 'Processing...' : 'Process Images' }}
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  onProcess: {
    type: Function,
    required: true
  }
})

const isProcessing = ref(false)

async function handleProcessImages() {
  isProcessing.value = true
  try {
    await props.onProcess()
  } catch (error) {
    console.error('Error processing images:', error)
    // You might want to show an error message to the user here
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
.process-images {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.el-button {
  margin-top: 20px;
}
</style>