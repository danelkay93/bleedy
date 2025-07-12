<template>
  <div class="bleed-adjustment">
    <label>Adjust Bleed Amount:</label>
    <div class="value-display">
      <wired-card elevation="1">
        {{ modelValue }} pixels
      </wired-card>
    </div>
    <div
      ref="sliderContainer"
      class="slider-container"
    >
      <wired-slider
        min="0"
        max="100"
        :value="modelValue"
        @change="$emit('update:modelValue', Number($event.target.value))"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {DEFAULT_BLEED_AMOUNT} from '../../config/appConfig'

const props = withDefaults(
  defineProps<{
    modelValue: number
  }>(),
  {
    modelValue: DEFAULT_BLEED_AMOUNT
  }
)

defineEmits<{
  (e: 'update:modelValue', value: number): void
}>()

const sliderContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  // Ensure wired-slider is properly styled
  const slider = sliderContainer.value?.querySelector('wired-slider')
  if (slider) {
    // Force roughness and style refresh
    slider.setAttribute('roughness', '2')
    // slider.requestUpdate?.()
  }
})
</script>

<style scoped>
.bleed-adjustment {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}

.value-display {
  display: flex;
  justify-content: center;
  margin: 0.5rem 0;
}

.value-display wired-card {
  --wired-card-background-color: transparent;
  padding: 0.5rem 1rem;
  font-family: 'Architects Daughter', cursive;
}

.slider-container {
  width: 100%;
  padding: 1rem 0;
}

:deep(wired-slider) {
  width: 100%;
  --wired-slider-knob-color: var(--el-color-primary);
  --wired-slider-bar-color: #666;
}

:deep(wired-slider)::part(knob) {
  fill: transparent;
  stroke: var(--el-color-primary);
  stroke-width: 2px;
}
</style>
