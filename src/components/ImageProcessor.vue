<template>
  <el-container class="image-processor container mx-auto" id="image-processor-component">
    <el-row>
      <el-col :span="24">
        <el-steps :active="activeStep" finish-status="success">
          <el-step title="Select Files"></el-step>
          <el-step title="Configure Settings"></el-step>
          <el-step title="Process Images"></el-step>
          <el-step title="Processing Results"></el-step>
        </el-steps>
      </el-col>
    </el-row>

    <!-- Step 1: Select Files -->
    <el-row v-if="activeStep === 0">
      <el-col :span="24">
        <h2 class="text-xl font-bold mb-4">Step 1: Select Image Files</h2>
        <el-button @click="openFilePicker" type="primary" class="mb-4">Open File Picker</el-button>
        <el-input v-model="searchQuery" placeholder="Search files..." class="mb-4" clearable>
          <template #prepend>
            <el-icon><i class="el-icon-search"></i></el-icon>
          </template>
        </el-input>
        <el-scrollbar class="mb-4" style="height: 200px; overflow-y: auto">
          <div v-if="filteredFiles.length > 0">
            <el-card
              v-for="(file, index) in filteredFiles"
              :key="index"
              class="mb-2"
              shadow="hover"
            >
              <div class="flex justify-between items-center">
                <span>{{ file.name }}</span>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="small"
                  @click="removeFile(index)"
                ></el-button>
              </div>
            </el-card>
          </div>
          <p v-else class="text-gray-500">No files selected.</p>
        </el-scrollbar>
        <el-button v-if="selectedFiles.length > 0" type="warning" @click="clearFiles"
          >Clear All Files</el-button
        >
      </el-col>
    </el-row>

    <!-- Step 2: Configure Settings -->
    <el-row v-if="activeStep === 1">
      <el-col :span="24">
        <h2 class="text-xl font-bold mb-4">Step 2: Configure Settings</h2>
        <label for="bleed-amount" class="block mb-2">Bleed Amount (px):</label>
        <input
          type="number"
          v-model="bleedAmount"
          id="bleed-amount"
          min="0"
          class="p-2 border rounded w-full"
        />
      </el-col>
    </el-row>

    <!-- Step 3: Process Images -->
    <el-row v-if="activeStep === 2">
      <el-col :span="24">
        <h2 class="text-xl font-bold mb-4">Step 3: Process Images</h2>
        <button @click="emitProcessEvent" class="p-2 bg-green-500 text-white rounded">
          Process Images
        </button>
      </el-col>
    </el-row>

    <!-- Step 4: Processing Results -->
    <el-row v-if="activeStep === 3">
      <el-col :span="24">
        <h2 class="text-xl font-bold mb-4">Step 4: Processing Results</h2>
        <el-scrollbar class="mt-4" style="height: 400px; overflow-y: auto">
          <div v-if="processedImages.length > 0">
            <el-card
              v-for="(image, index) in processedImages"
              :key="index"
              class="mb-4"
              shadow="hover"
            >
              <img :src="image" :style="getThumbnailStyle(image)" alt="Processed Image" />
            </el-card>
          </div>
          <p v-else class="text-gray-500">No processed images available.</p>
        </el-scrollbar>
        <el-button v-if="processedImages.length > 0" type="primary" @click="saveAsZip"
          >Save All as ZIP</el-button
        >
      </el-col>
    </el-row>

    <!-- Navigation Buttons -->
    <el-row class="flex justify-between mt-6">
      <el-col :span="12">
        <el-button @click="prevStep" :disabled="activeStep === 0">Previous</el-button>
      </el-col>
      <el-col :span="12" class="text-right">
        <el-button @click="nextStep" :disabled="activeStep === 3">Next</el-button>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
import * as zip from '@zip.js/zip.js'

export default {
  data() {
    return {
      activeStep: 0,
      selectedFiles: [],
      searchQuery: '',
      bleedAmount: 10,
      processedImages: []
    }
  },
  computed: {
    filteredFiles() {
      if (!this.searchQuery) return this.selectedFiles
      return this.selectedFiles.filter((file) =>
        file.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    }
  },
  methods: {
    nextStep() {
      if (this.activeStep < 3) this.activeStep++
    },
    prevStep() {
      if (this.activeStep > 0) this.activeStep--
    },
    openFilePicker() {
      const options = {
        types: [
          {
            description: 'Image Files',
            accept: {
              'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp']
            }
          }
        ],
        multiple: true
      }
      window
        .showOpenFilePicker(options)
        .then((fileHandles) => Promise.all(fileHandles.map((handle) => handle.getFile())))
        .then((files) => {
          this.selectedFiles = files
        })
        .catch((err) => console.error('Error selecting files:', err))
    },
    removeFile(index) {
      this.selectedFiles.splice(index, 1)
    },
    clearFiles() {
      this.selectedFiles = []
    },
    emitProcessEvent() {
      this.$emit('process-images', {
        files: this.selectedFiles,
        bleedAmount: this.bleedAmount
      })
    },
    getThumbnailStyle(image) {
      const img = new Image()
      img.src = image

      return new Promise((resolve) => {
        img.onload = () => {
          let width = img.width
          let height = img.height

          if (width > height) {
            if (width > this.maxThumbnailSize) {
              height *= this.maxThumbnailSize / width
              width = this.maxThumbnailSize
            }
          } else {
            if (height > this.maxThumbnailSize) {
              width *= this.maxThumbnailSize / height
              height = this.maxThumbnailSize
            }
          }

          resolve({
            width: `${width}px`,
            height: `${height}px`
          })
        }
      })
    },
    saveAsZip() {
      // Logic to save all processed images as a ZIP file
    }
  }
}
</script>
