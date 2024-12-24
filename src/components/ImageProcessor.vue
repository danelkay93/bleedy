<template>
  <div class="image-bleed-processor">
    <StepManager 
      :steps="processorSteps" 
      v-model="activeStep"
      :is-next-disabled="activeStep === 0 && selectedImages.length === 0"
    >
      <template #default="{ activeStep }">
        <div class="step-content">
          <h2 class="step-title">{{ processorSteps[activeStep].title }}</h2>
          <wired-card elevation="2">
            <div class="step-content-inner">
              <ImageSelection 
                v-if="activeStep === 0"
                :activeStep="activeStep" 
                @update:selected-images="updateSelectedImages"
              />
              <BleedAdjustment
                v-else-if="activeStep === 1"
                v-model="bleedAmount"
              />
              <ProcessImages
                v-else-if="activeStep === 2"
                :images="selectedImages"
                :bleed-amount="bleedAmount"
                @process-complete="handleProcessComplete"
              />
              <ReviewResults
                v-else-if="activeStep === 3"
                :images="processedImages"
                @save="saveAsZip"
              />
            </div>
          </wired-card>
        </div>
      </template>
    </StepManager>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import StepManager from './StepManager.vue'
import ImageSelection from './ImageSelection.vue'
import BleedAdjustment from './steps/BleedAdjustment.vue'
import ProcessImages from './steps/ProcessImages.vue'
import ReviewResults from './steps/ReviewResults.vue'
import { processorSteps } from '../config/processorSteps'
import 'wired-elements'

const activeStep = ref(0)
const bleedAmount = ref(50)
const processedImages = ref<string[]>([])
const selectedImages = ref<File[]>([])

const updateSelectedImages = (images: File[]) => {
  selectedImages.value = images
}

const handleProcessComplete = (images: string[]) => {
  processedImages.value = images
}

const saveAsZip = () => {
  console.log('Saving processed images as ZIP')
  // Implement ZIP saving logic here
}
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
  max-width: 1000px;
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

.wired-card {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto 20px;
  padding: 20px;
}
</style>
