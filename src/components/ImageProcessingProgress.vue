<template>
  <wired-card elevation="2" class="progress-card">
    <div class="progress-content">
      <wired-progress :value="progress" :max="100"></wired-progress>
      
      <div class="status-details">
        <div class="status-row files">
          <wired-icon-button>📁</wired-icon-button>
          <span>{{ processedCount }} / {{ totalFiles }} files</span>
        </div>
        
        <div class="status-row time">
          <wired-icon-button>⏱️</wired-icon-button>
          <span>Elapsed: {{ formatTime(elapsedTime) }}</span>
        </div>
        
        <div class="status-row estimate">
          <wired-icon-button>🎯</wired-icon-button>
          <span>Remaining: {{ formatTime(remainingTime) }}</span>
        </div>
      </div>
    </div>
  </wired-card>
</template>

<script setup lang="ts">
import {WiredProgress} from 'wired-elements'

const props = defineProps<{
  progress: number
  processedCount: number
  totalFiles: number
  elapsedTime: number
  remainingTime: number
}>()

function formatTime(seconds: number): string {
  if (!seconds || isNaN(seconds)) return '...'
  const mins = Math.floor(seconds / 60)
  const secs = Math.round(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.progress-card {
  width: 100%;
  --wired-progress-color: #000;
  --wired-progress-label-color: #000;
  font-family: 'Architects Daughter', cursive;
}

.progress-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

:deep(wired-progress) {
  width: 100%;
}

.status-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

:deep(wired-icon-button) {
  --wired-icon-size: 16px;
  font-size: 14px;
}
</style>
