<template>
  <div class="file-uploader">
    <h2>Upload Image</h2>
    <input type="file" @change="handleFileUpload" />
    <button @click="processImageWithBleed">Process Image</button>
    <div v-if="resultImagePath">
      <h3>Processed Image:</h3>
      <img :src="resultImagePath" alt="Processed Image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      bleedAmount: 20,  // Example value
      resultImagePath: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async processImageWithBleed() {
      if (this.selectedFile) {
        const filePath = this.selectedFile.name;
        // Example of interacting with PyScript
        await pyodide.runPythonAsync(`
            from charles import add_bleed_to_image
            result_path = add_bleed_to_image("${filePath}", ${this.bleedAmount})
        `);
        this.resultImagePath = pyodide.globals.get('result_path');
      } else {
        alert('Please select a file first!');
      }
    }
  }
};
</script>

<style scoped>
.file-uploader {
  text-align: center;
  margin-top: 20px;
}
</style>
