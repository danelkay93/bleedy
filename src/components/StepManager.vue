<template>


  <div class="step-manager">
<el-row justify="center">
  <el-col class="col" :span="14">
    <el-steps :simple="true" :active="activeStep" finish-status="success" simple>
      <el-step
        v-for="(step, index) in steps"
        :key="step.title"
        :title="step.title"
        @click="handleStepClick(index)"
        :class="{ 'clickable': canNavigateToStep(index) }"
      >
        <template #icon>
          <div class="step-icon">
            <wired-checkbox
              :checked="index < activeStep"
              disabled
              :class="{
                'current-step': index === activeStep,
                'completed-step': index < activeStep
              }"
            />
          </div>
        </template>
      </el-step>
    </el-steps>

    <div class="step-content">
      <slot :activeStep="activeStep" />
    </div>
    <div class="navigation-buttons">
      <wired-button
        v-show="activeStep > 0"
        @click="prevStep"
      >
        Previous
      </wired-button>
      <wired-button
        v-if="activeStep < steps.length - 1"
        @click="nextStep"
        :class="{ 'disabled': isNextDisabled }"
        :style="{
          opacity: isNextDisabled ? '0.5' : '1',
          pointerEvents: isNextDisabled ? 'none' : 'auto'
        }"
      >
        Next
      </wired-button>
    </div>
      </el-col>

   </el-row>
  </div>



</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import {WiredButton, WiredCheckbox } from 'wired-elements';

const props = defineProps<{
  steps: Array<{ title: string }>,
  modelValue: number,
  isNextDisabled: boolean
}>()

const emit = defineEmits(['update:modelValue'])

const activeStep = ref(props.modelValue)

watch(() => props.modelValue, (newValue) => {
  activeStep.value = newValue
})

function nextStep() {
  if (activeStep.value < props.steps.length - 1 && !props.isNextDisabled) {
    activeStep.value++
    emit('update:modelValue', activeStep.value)
  }
}

const completedSteps = ref([0])

function canNavigateToStep(stepIndex: number) {
  return stepIndex <= activeStep.value + 1 && (stepIndex <= Math.max(...completedSteps.value) || stepIndex === activeStep.value + 1)
}

watch(activeStep, (newStep) => {
  if (!completedSteps.value.includes(newStep)) {
    completedSteps.value.push(newStep)
  }
})

function handleStepClick(stepIndex: number) {
  if (canNavigateToStep(stepIndex)) {
    activeStep.value = stepIndex
    emit('update:modelValue', stepIndex)
  }
}

function prevStep() {
  if (activeStep.value > 0) {
    activeStep.value--
    emit('update:modelValue', activeStep.value)
  }
}
</script>

<style scoped>
.step-manager {
  width: 100%;
  margin: 0 auto;
  padding: 10px;
}

.step-content {
  margin: 20px 0;
}

.navigation-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
  padding: 10px;
  position: relative;
  z-index: 1;
}

.navigation-buttons wired-button {
  min-width: 100px;
}

.clickable {
  cursor: pointer;
}

.el-step:not(.clickable) {
  opacity: 0.5;
  pointer-events: none;
}

.step-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.col {
  width: 100%;
}

:deep(wired-checkbox[disabled]) {
  opacity: 1;
}

:deep(.current-step) {
  transform: scale(1.2);
  filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
}

:deep(.current-step)::before {
  content: '';
  position: absolute;
  inset: -4px;
  border: 2px solid #000;
  border-radius: 4px;
  opacity: 0.3;
  transform: rotate(-2deg);
}

:deep(.completed-step) {
  --wired-checkbox-color: var(--el-color-success);
}
</style>
