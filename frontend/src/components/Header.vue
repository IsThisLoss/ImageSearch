<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-2 shadow">
  <div class="container-fluid justify-content-center">
    <SearchBar
      @searchSubmit="searchSubmit"
    />
  </div>
</nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import SearchBar from './SearchBar.vue'

export default defineComponent({
  name: 'Header',
  components: {
    SearchBar,
  },
  methods: {
    searchSubmit(text: string) {
      this.$emit("searchSubmit", text)
    }
  },
});

</script>
