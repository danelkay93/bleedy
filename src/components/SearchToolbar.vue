<template>
  <div class="toolbar">
    <wired-button elevation="2" @click="$emit('browse')">
      Browse
    </wired-button>

    <wired-search-input
      placeholder="Search Images..."
      :value="searchQuery"
      @input="$emit('update:searchQuery', $event.target.value)"
      class="search-input"
    ></wired-search-input>

    <div class="sort-select">
      <label for="sort">Sort By:</label>
      <wired-combo 
        id="sort" 
        :selected="sortOption"
        @selected="$emit('update:sortOption', $event.detail.selected)"
      >
        <wired-item value="name">Name</wired-item>
        <wired-item value="date">Date Modified</wired-item>
        <wired-item value="size">Size</wired-item>
      </wired-combo>
    </div>
  </div>
</template>

<script>
import 'wired-elements';

export default {
  name: 'SearchToolbar',
  props: {
    searchQuery: {
      type: String,
      required: true
    },
    sortOption: {
      type: String,
      required: true
    }
  },
  emits: ['browse', 'update:searchQuery', 'update:sortOption']
}
</script>

<style scoped>
.toolbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input {
  width: 200px;
  background: transparent !important;
}

.sort-select {
  display: flex;
  align-items: center;
}

.sort-select label {
  margin-right: 0.5rem;
}

:deep(wired-combo) {
  --wired-combo-popup-bg: #ffffff;
  background: transparent;
  z-index: 1000;
}

:deep(wired-item) {
  padding: 8px;
  background: #ffffff;
  color: #000000;
  display: block;
  margin: 4px 0;
}

:deep(wired-item:hover) {
  background: #f0f0f0;
}
</style>
