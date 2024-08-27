<template>
  <div id="app">
    <ImageProcessor id="image-processor-component" />
  </div>
</template>

<script>
import ImageProcessor from './components/ImageProcessor.vue'

export default {
  name: 'App',
  components: {
    ImageProcessor
  }
}
</script>

<!--<style>-->
<!--#app {-->
<!--  font-family: Avenir, Helvetica, Arial, sans-serif;-->
<!--  text-align: center;-->
<!--  margin-top: 60px;-->
<!--}-->
<!--</style>-->
