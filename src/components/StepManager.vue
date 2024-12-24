<template>
  <div class="step-manager">
    <!-- Progress Bar -->
    <wired-card elevation="0" fill="teal" class="progress-bar">
      <el-steps :active="activeStep" finish-status="success" class="custom-steps" simple>
        <el-step v-for="(step, index) in steps" :key="step.name">
          <template #icon>
            <el-icon class="step-icon" :size="45">
              <component :is="getStepIconComponent(index)" />
            </el-icon>
          </template>
        </el-step>
      </el-steps>
    </wired-card>

    <!-- Title Slot -->
    <div class="title">
      <slot name="title" :activeStep="activeStep" :currentTitle="steps[activeStep].title">
        <!-- Default title content (if any) -->
      </slot>
    </div>

    <!-- Content Slot -->
    <div class="content">
      <slot name="content" :activeStep="activeStep">
        <!-- Default content (if any) -->
      </slot>
    </div>

    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <slot name="navigation" :prevStep="prevStep" :nextStep="nextStep" :activeStep="activeStep">
        <!-- Custom navigation buttons -->
        <wired-icon-button @click="prevStep" :disabled="activeStep === 0">
          <LeftArrowIcon />
        </wired-icon-button>
        <wired-icon-button @click="nextStep" :disabled="activeStep === steps.length - 1">
          <RightArrowIcon />
        </wired-icon-button>
      </slot>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import LeftArrowIcon from '../assets/sketch_icons/left-arrow.vue'
import RightArrowIcon from '../assets/sketch_icons/right-arrow.vue'
import ImageSelectionIcon from '../assets/sketch_icons/image-selection.vue'
import BleedSettingsIcon from '../assets/sketch_icons/bleed-settings.vue'
import BloodDropletIcon from '../assets/sketch_icons/blood-droplet.vue'
import StarsIcon from '../assets/sketch_icons/stars.vue'
import CheckMarkIcon from '../assets/sketch_icons/check-mark.vue'
import { WiredIconButton } from 'wired-elements'

export default {
  components: {
    WiredIconButton,
    LeftArrowIcon,
    RightArrowIcon,
    ImageSelectionIcon,
    BleedSettingsIcon,
    BloodDropletIcon,
    StarsIcon,
    CheckMarkIcon
  },
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

    watch(
      () => props.modelValue,
      (newValue) => {
        activeStep.value = newValue
      }
    )

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

    const iconComponents = {
      'image-selection-icon': ImageSelectionIcon,
      'bleed-settings-icon': BleedSettingsIcon,
      'blood-droplet-icon': BloodDropletIcon,
      'stars-icon': StarsIcon
    }

    function getStepIconComponent(index) {
      if (activeStep.value > index) {
        return CheckMarkIcon
      } else {
        const iconName = props.steps[index].iconName
        return iconComponents[iconName]
      }
    }

    return {
      activeStep,
      nextStep,
      prevStep,
      getStepIconComponent
    }
  }
}
</script>

<style scoped>
@import '../../node_modules/doodle.css/doodle.css';
@import '../assets/handdrawn.css';
@import 'papercss/dist/paper.min.css';

.step-manager {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.progress-bar {
  align-items: center;
  width: 100%;
  max-width: 800px;
  text-align: center;
  font-size: 3em;
  font-weight: bold;
  /* transparent fill color */
  --el-fill-color-light: transparent;
}

.custom-steps {
  --el-step-border-radius: 2;
  --el-step-icon-size: 80px;
}

.custom-steps .el-step {
  font-family: 'Doodle', sans-serif;
}

.custom-steps .el-step__title {
  font-size: 3em;
}

.step-icon {
    background-color: transparent; /* Transparent background to let the SVG shape define the glow */
}

.step-icon svg {
      filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.6)); /* Glow around the SVG shape */
}
.navigation-buttons {
  margin-top: 20px;
}

.navigation-buttons wired-icon-button {
  margin: 0 10px;
}

body {
  font-family: 'Doodle', sans-serif;
}
</style>
