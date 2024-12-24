<template>
  <div>
    <wired-button @click="$emit('process')">Process Images</wired-button>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  (e: 'process'): void
}>()
</script>
