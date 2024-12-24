<template>
  <div>
    <label>Adjust Bleed Amount:</label>
    <wired-slider 
      min="0" 
      max="100" 
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: number
}>()

defineEmits<{
  (e: 'update:modelValue', value: number): void
}>()
</script>
