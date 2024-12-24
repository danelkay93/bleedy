<template>
  <div class="image-processor-wrapper">
    <StepManager 
      :steps="steps" 
      v-model="activeStep"
      :is-next-disabled="activeStep === 0 && selectedImages.length === 0"
    >
      <template #default="{ activeStep }">
        <div class="step-content">
          <h2 class="step-title">{{ steps[activeStep].title }}</h2>
          <wired-card elevation="2">
            <div class="step-content-inner">
              <!-- Step-specific content -->
              <div v-if="activeStep === 0">
                <ImageSelection 
                  :activeStep="activeStep" 
                  @update:selected-images="updateSelectedImages"
                />
              </div>
              <div v-else-if="activeStep === 1">
                <label>Adjust Bleed Amount:</label>
                <wired-slider min="0" max="100" v-model="bleedAmount"></wired-slider>
              </div>
              <div v-else-if="activeStep === 2">
                <wired-button @click="processImages">Process Images</wired-button>
              </div>
              <div v-else-if="activeStep === 3">
                <p>Review your processed images below:</p>
                <div class="image-gallery">
                  <img
                    v-for="(img, index) in processedImages"
                    :key="index"
                    :src="img"
                    alt="Processed Image" />
                </div>
                <wired-button @click="saveAsZip">Save as ZIP</wired-button>
              </div>
            </div>
          </wired-card>
          
        </div>
      </template>
    </StepManager>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StepManager from './StepManager.vue'
import ImageSelection from './ImageSelection.vue' // Import the ImageSelection component
import 'wired-elements'

const steps = [
  {
    name: 'Select Images',
    title: 'Select',
    iconName: 'image-selection-icon'
  },
  {
    name: 'Adjust Bleed',
    title: 'Settings',
    iconName: 'bleed-settings-icon'
  },
  {
    name: 'Process Images',
    title: 'Bleed!',
    iconName: 'blood-droplet-icon'
  },
  {
    name: 'Review Results',
    title: 'Results',
    iconName: 'stars-icon'
  }
]

const activeStep = ref(0)
const bleedAmount = ref(50)
const processedImages = ref([])
const selectedImages = ref([])

const updateSelectedImages = (images) => {
  selectedImages.value = images
}

// Methods
function processImages() {
  console.log('Processing images with bleed amount:', bleedAmount.value)
  // Implement your image processing logic here
}

function saveAsZip() {
  console.log('Saving processed images as ZIP')
  // Implement ZIP saving logic here
}
</script>

<style scoped>
@import '../../node_modules/doodle.css/doodle.css';
@import '../assets/handdrawn.css';
@import 'papercss/dist/paper.min.css';

.image-processor-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
}

.step-content {
  width: 100%;
  max-width: 800px;
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
  max-width: 800px;
  width: 100%;
  margin: 0 auto 20px;
  padding: 20px;
}


.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-gallery img {
  max-width: 100%;
  height: auto;
  border: 2px dashed #000;
}

body {
  font-family: 'Doodle', sans-serif;
  background-color: #fafafa;
}
</style>
