<template>
  <div id="file-picker-component" class="file-picker">
    <h2>Select Image Files</h2>
    <button @click="openFilePicker">Open File Picker</button>
    <div v-if="selectedFileNames.length">
      <h3>Selected Files:</h3>
      <ul>
        <li v-for="(file, index) in selectedFileNames" :key="index">{{ file }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFiles: [],
      selectedFileNames: []
    };
  },
  methods: {
    async openFilePicker() {
      try {
        const options = {
          types: [{
            description: 'Image Files',
            accept: {
              'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp']
            }
          }],
          multiple: true
        };
        const fileHandles = await window.showOpenFilePicker(options);
        this.selectedFiles = await Promise.all(fileHandles.map(handle => handle.getFile()));
        this.selectedFileNames = this.selectedFiles.map(file => file.name);

        // Emit a custom event with the selected files
        const event = new CustomEvent('files-selected', { detail: this.selectedFiles });
        window.dispatchEvent(event);
      } catch (err) {
        console.error('Error selecting files:', err);
      }
    }
  }
};
</script>

<style scoped>
.file-picker {
  text-align: center;
  margin-top: 20px;
}
button {
  margin-top: 10px;
}
</style>
