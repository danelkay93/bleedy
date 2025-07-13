<template>
  <span>
    <template
      v-for="(part, index) in parts"
      :key="index"
    >
      <mark v-if="part.highlight">{{ part.text }}</mark>
      <template v-else>{{ part.text }}</template>
    </template>
  </span>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'

export default defineComponent({
  name: 'HighlightedText',
  props: {
    text: {
      type: String,
      required: true
    },
    query: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const parts = computed(() => {
      if (!props.query) {
        return [{ text: props.text, highlight: false }]
      }
      const regex = new RegExp(`(${props.query})`, 'gi')
      const result = []
      let lastIndex = 0
      props.text.replace(regex, (match, _, index) => {
        if (index > lastIndex) {
          result.push({ text: props.text.substring(lastIndex, index), highlight: false })
        }
        result.push({ text: match, highlight: true })
        lastIndex = index + match.length
      })
      if (lastIndex < props.text.length) {
        result.push({ text: props.text.substring(lastIndex), highlight: false })
      }
      return result
    })

    return {
      parts
    }
  }
})
</script>

<style scoped>
mark {
  background-color: #ffff00;
  color: #000;
  padding: 0 2px;
  border-radius: 2px;
}
</style>
