<template>
  <div class="bleed-adjustment">
    <h3>Adjust Bleed Amount</h3>
    <el-slider
      v-model="localBleedAmount"
      range
      :min="0"
      :max="100"
      :marks="marks"
      @change="updateBleedAmount"
    >
      <template #default="{ value }">
        <div class="slider-label">{{ value }}</div>
      </template>
    </el-slider>
    <p>Current bleed range: {{ localBleedAmount[0] }}px - {{ localBleedAmount[1] }}px</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [0, 100]
  }
})

const emit = defineEmits(['update:modelValue'])

const localBleedAmount = ref(props.modelValue)

const marks = {
  0: '0px',
  25: '25px',
  50: '50px',
  75: '75px',
  100: '100px'
}

watch(() => props.modelValue, (newValue) => {
  localBleedAmount.value = newValue
})

function updateBleedAmount(value) {
  emit('update:modelValue', value)
}
</script>

<style scoped>
.bleed-adjustment {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.slider-label {
  font-size: 12px;
  color: #606266;
}
</style>