import {saveAs} from 'file-saver'
import JSZip from 'jszip'

export function useImageDownload() {
  async function downloadImage(imageUrl: string, index: number) {
    const response = await fetch(imageUrl)
    const blob = await response.blob()
    saveAs(blob, `processed-image-${index + 1}.${blob.type.split('/')[1]}`)
  }

  async function downloadZip(images: string[] | readonly string[]) {
    const zip = new JSZip()
    const imageArray = Array.from(images)

    await Promise.all(
      imageArray.map(async (imageUrl, index) => {
        const response = await fetch(imageUrl)
        const blob = await response.blob()
        zip.file(`processed-image-${index + 1}.${blob.type.split('/')[1]}`, blob)
      })
    )

    const content = await zip.generateAsync({type: 'blob'})
    saveAs(content, 'processed-images.zip')
  }

  return {
    downloadImage,
    downloadZip
  }
}
