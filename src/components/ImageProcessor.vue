<template>
  <div class="image-processor-wrapper">
    <StepManager :steps="steps" v-model="activeStep">
      <el-row justify="center">
        <!-- Slot for progress bar -->
        <template #progress="{ activeStep }"></template>
      </el-row>
      <el-row justify-center>
        <!-- Slot for title -->
        <template #title="{ activeStep }">
          <h1 class="step-title">{{ steps[activeStep].title }}</h1>
        </template>
      </el-row>


        <!-- Slot for content -->
        <template #content="{ activeStep }">
          <wired-card>
                  <el-row justify="center">
        <el-col :span="24">
            <!-- Step-specific content -->
            <div v-if="activeStep === 0">
              <!-- Include ImageSelection component -->
              <ImageSelection :activeStep="activeStep" />
            </div>
            <div v-else-if="activeStep === 1">
              <!-- Step 2: Wired Slider -->
              <label>Adjust Bleed Amount:</label>
              <wired-slider min="0" max="100" v-model="bleedAmount"></wired-slider>
            </div>
            <div v-else-if="activeStep === 2">
              <!-- Step 3: Wired Button for Actions -->
              <wired-button @click="processImages">Process Images</wired-button>
            </div>
            <div v-else-if="activeStep === 3">
              <!-- Step 4: Review Results -->
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
                    </el-col>
      </el-row>
          </wired-card>
        </template>

      <el-row justify-center>
        <!-- Slot for navigation buttons -->
        <template #navigation="{ prevStep, nextStep, activeStep }">
          <!-- Custom navigation buttons -->
          <div class="navigation-buttons">
            <wired-button v-if="activeStep > 0" @click="prevStep">Previous</wired-button>
            <wired-button v-if="activeStep < steps.length - 1" @click="nextStep">Next</wired-button>
          </div>
        </template>
      </el-row>
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
  min-height: 100vh;
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

.navigation-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.navigation-buttons wired-button {
  margin: 0 10px;
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
