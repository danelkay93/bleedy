<template>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose">
    <el-menu-item index="1" @click="removeSelectedFiles">
      <el-icon id="remove-icon"><remove-filled /></el-icon>
      <template #title>Remove Selected</template>
    </el-menu-item>
    <el-menu-item index="2" @click="clearFiles">
      <el-icon><delete /></el-icon>
      <template #title>Remove All</template>
    </el-menu-item>
    <el-menu-item index="3">
      <el-icon><setting /></el-icon>
      <template #title>Navigator Four</template>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Setting, RemoveFilled, Delete
} from '@element-plus/icons-vue'

const isCollapse = ref(true)
const selectedImages = ref<string[]>([])
const images = ref<{ id: string }[]>([])
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
function removeSelectedFiles() {
  images.value = images.value.filter((image) => !selectedImages.value.includes(image.id))
  selectedImages.value = []
}

function clearFiles() {
  images.value = []
  selectedImages.value = []
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

#remove-icon {
  color: #e53935;
}
</style>
