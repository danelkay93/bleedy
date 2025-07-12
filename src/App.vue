<!-- App.vue -->
<template>
  <div class="common-layout">
    <el-container>
      <el-header height="6.5">
        <el-row>
          <div
            class="header-content"
            :style="{backgroundImage: svgBackground}"
          >
            <div class="logo-container">
              <Logo class="logo" />
              <p class="app-name cabin-sketch-bold">
                bleedy.py
              </p>
            </div>
          </div>
        </el-row>
      </el-header>
      <el-main>
        <el-row justify="center">
          <el-col
            class="step-row"
            :span="12"
          >
            <router-view />
          </el-col>
        </el-row>
      </el-main>
      <el-footer>
        <el-row
          justify="center"
          align="middle"
        >
          <div class="footer-content">
            Based on bleedy.py, by North101 and OliviaJuliet.
            <br>
            Created by Buteremelse.
            <br>
            This website is not produced, endorsed, supported, or affiliated with Fantasy Flight
            Games.
          </div>
        </el-row>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import rough from 'roughjs'
import Logo from './components/Logo.vue'

const svgBackground = ref('') // Store the encoded SVG background

// Function to serialize and encode the generated SVG
const serializeSVG = (svg) => {
  const svgData = new XMLSerializer().serializeToString(svg)
  const encodedSvg = encodeURIComponent(svgData).replace(/#/g, '%23').replace(/"/g, "'")
  return `url('data:image/svg+xml,${encodedSvg}')`
}

// Function to generate the Rough.js SVG
const generateSvgBackground = (container) => {
  // Create an SVG element to use with Rough.js
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
  svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  svg.setAttribute('width', '100%') // Ensure SVG spans full width
  svg.setAttribute('height', '100%') // Ensure SVG spans full height

  // Initialize Rough.js with the SVG root
  const rc = rough.svg(svg)

  // Get the actual container dimensions for the rectangle
  const width = container.clientWidth
  const height = container.clientHeight

  // Create a Rough.js rectangle
  const rect = rc.rectangle(0, 0, width, height, {
    fill: '#1a4d80', // Blue color for header background
    roughness: 3, // Sketchy edges
    fillStyle: 'solid' // Solid fill
  })

  // Append the rectangle to the SVG
  svg.appendChild(rect)

  // Serialize and encode the SVG to use it as a background image
  svgBackground.value = serializeSVG(svg)
}

onMounted(() => {
  nextTick(() => {
    const container = document.querySelector('.header-content')

    if (container) {
      // Initial generation of the SVG background
      generateSvgBackground(container)

      // ResizeObserver to handle dynamic resizing of the container
      const resizeObserver = new ResizeObserver(() => {
        generateSvgBackground(container)
      })

      // Observe the container for resizing
      resizeObserver.observe(container)
    }
  })
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cabin+Sketch:wght@400;700&display=swap');

/* Common layout styles */
.common-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.cabin-sketch-regular {
  font-family: 'Cabin Sketch', sans-serif;
  font-weight: 400;
  font-style: normal;
}

:root {
  --el-header-height: 8rem; /* Set header height */
}

.app-name {
  font-family: 'Cabin Sketch', sans-serif;
  font-weight: 700;
  font-style: normal;
  font-size: 7rem;
}

/* Header styles */
el-header {
  height: 100%; /* Use custom header height */
  width: 100%;
  display: flex;
  flex-direction: column; /* Use flexbox to control layout */
  background-color: var(--primary-dark);
  padding: 0;
  --el-header-height: '6.5rem'; /* Set header height */
  min-height: '6.5rem';
}

.header-content {
  align-items: center;
  width: 100%; /* Ensure header content takes the full width */
  height: 100%;
  background-size: cover; /* Cover the entire header with the SVG */
  background-repeat: no-repeat; /* Prevent repeating */
  margin-top: 0;
  margin-left: 0;
  min-height: '6.5rem';
}

.logo-container {
  display: flex;
  align-items: center;
  z-index: 1;
}

.logo {
  height: 6rem;
  width: auto;
}

.step-row {
  width: 100%;
  border-radius: 4px;
}

.app-name {
  font-weight: bold;
  font-size: 4.8em;
  color: black;
  margin: 0 0 0 0.2em; /* Add left margin for spacing */
  z-index: 1;
}

/* Main content styles */
el-main {
  flex: 1;
  display: flex;
  justify-content: center;
  background-color: var(--background-light);
  padding: 20px;
}

/* Footer styles */
el-footer {
  background-color: var(--primary-dark);
  padding: 10px 20px;
}

.footer-content {
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-light);
  font-family: 'Doodle', sans-serif;
}

/* Body styles */
body {
  margin: 0;
  padding: 0;
  font-family: 'Doodle', sans-serif;
  background-color: var(--background-light);
}
</style>
