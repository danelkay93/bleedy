<template>
  <div class="step-manager">
    <el-steps :active="activeStep" finish-status="success" simple>
      <el-step v-for="step in steps" :key="step.title" :title="step.title" />
    </el-steps>
    
    <div class="step-content">
      <slot :activeStep="activeStep" />
    </div>
    
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  props: {
    steps: {
      type: Array,
      required: true
    },
    modelValue: {
      type: Number,
      default: 0
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const activeStep = ref(props.modelValue)

    watch(() => props.modelValue, (newValue) => {
      activeStep.value = newValue
    })

    function nextStep() {
      if (activeStep.value < props.steps.length - 1) {
        activeStep.value++
        emit('update:modelValue', activeStep.value)
      }
    }

    function prevStep() {
      if (activeStep.value > 0) {
        activeStep.value--
        emit('update:modelValue', activeStep.value)
      }
    }

    return {
      activeStep,
      nextStep,
      prevStep
    }
  }
}
</script>

<style scoped>
.step-manager {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.step-content {
  margin: 20px 0;
}

.step-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
