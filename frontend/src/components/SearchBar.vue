<template>
  <form @submit.prevent.stop="submit" class="d-inline-block mx-auto my-2 navbar-form" id="search" role="search">
  <div class="input-group">
      <input 
        class="form-control mr-sm-1"
        placeholder="Search for..."
        type="search"
        aria-label="Search"
        v-model.trim="searchText"
      />
    <div class="input-group-append">
        <button class="btn btn-primary" type="submit">
            <i class="fas fa-search fa-sm"></i>
        </button>
    </div></div>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SearchBar',
  data() {
    return {
      searchText: ''
    }
  },
  methods: {
    submit() {
      this.$emit("searchSubmit", this.searchText)
    }
  },
});

</script>
