<template>
  <div class="image-bleed-processor">
    <StepManager
      v-model="activeStep"
      :steps="processorSteps.map((step) => ({title: step.title}))"
      :is-next-disabled="activeStep === 0 && selectedImages.length === 0">
      <template #default="{currentStep}">
        <div class="step-content">
          <h2 class="step-title">
            {{ processorSteps[currentStep].title }}
          </h2>
          <wired-card elevation="2">
            <div class="step-content-inner">
              <ImageSelection
                v-if="currentStep === 0"
                :active-step="currentStep"
                @update:selected-images="updateSelectedImages" />
              <BleedAdjustment v-else-if="currentStep === 1" v-model="bleedAmount" />
              <ProcessImages
                v-else-if="currentStep === 2"
                :images="selectedImages"
                :bleed-amount="bleedAmount"
                @process-complete="handleProcessComplete" />
              <ReviewResults v-else-if="currentStep === 3" :images="processedImages" />
            </div>
          </wired-card>
        </div>
      </template>
    </StepManager>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {DEFAULT_BLEED_AMOUNT} from '../config/appConfig'
import StepManager from './StepManager.vue'
import ImageSelection from './ImageSelection.vue'
import BleedAdjustment from './steps/BleedAdjustment.vue'
import ProcessImages from './steps/ProcessImages.vue'
import ReviewResults from './steps/ReviewResults.vue'
import {processorSteps} from '../config/processorSteps'
import {WiredCard} from 'wired-elements'

const activeStep = ref(0)
const bleedAmount = ref(DEFAULT_BLEED_AMOUNT)
const processedImages = ref<string[]>([])
const selectedImages = ref<File[]>([])

const updateSelectedImages = (images: File[]) => {
  selectedImages.value = images
}

const handleProcessComplete = (images: string[]) => {
  processedImages.value = images
}

// Removed unused saveAsZip method
</script>

<style scoped>
.image-bleed-processor {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
}

.step-content {
  width: 100%;
  margin: 0 auto;
}

.step-content-inner {
  padding: 20px;
}

.step-title {
  font-size: 2em;
  color: #333;
  margin: 20px 0;
}

wired-card {
  width: 100%;
  margin: 0 auto 20px;
  padding: 20px;
}
</style>
