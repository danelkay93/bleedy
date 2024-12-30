<template>
  <div class="toolbar">
    <el-button 
      class="browse-button"
      @click="$emit('browse')"
      type="primary"
    >
      Browse
    </el-button>

    <el-input
      v-model="localSearchQuery"
      placeholder="Search Images..."
      class="search-input"
      clearable
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'

const props = defineProps<{
  searchQuery: string
}>()

const emit = defineEmits<{
  (e: 'browse'): void
  (e: 'update:searchQuery', value: string): void
}>()

const localSearchQuery = ref(props.searchQuery)

watch(localSearchQuery, (newValue) => {
  emit('update:searchQuery', newValue)
})

watch(() => props.searchQuery, (newValue) => {
  localSearchQuery.value = newValue
})
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  flex-wrap: nowrap;
}

.search-input {
  width: 200px;
}
</style>
