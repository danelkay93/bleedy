// public/js/bleedy_interop.js

/**
 * Dispatches a custom event to inform the Vue application that an image has been processed.
 * @param {string} name - The name of the processed image file.
 * @param {string} blobUrl - The blob URL of the processed image.
 * @param {string} format - The format of the processed image (e.g., 'PNG', 'JPEG').
 */
export function dispatchProcessedImageToVue(name, blobUrl, format) {
  console.log(`JS interop: dispatching processed image - Name: ${name}, Format: ${format}`)
  const event = new CustomEvent('bleedy-image-processed', {
    detail: {
      name,
      blobUrl,
      format
    }
  })
  window.dispatchEvent(event)
}

/**
 * Dispatches a custom event to update the Vue application on processing progress.
 * @param {object} progressDetail - The progress detail object.
 * @param {number} progressDetail.progress - Overall progress percentage.
 * @param {number} progressDetail.processed - Number of files processed.
 * @param {number} progressDetail.total - Total number of files.
 * @param {number} progressDetail.elapsed - Elapsed time in seconds.
 * @param {number} progressDetail.remaining - Estimated remaining time in seconds.
 */
export function dispatchProgressToVue(progressDetail) {
  // console.log('JS interop: dispatching progress', progressDetail); // Can be noisy
  const event = new CustomEvent('processing-progress', {
    detail: progressDetail
  })
  window.dispatchEvent(event)
}

// Log to confirm the module is loaded by PyScript
console.log('bleedy_interop.js loaded')
