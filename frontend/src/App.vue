<template>
  <div id="wrapper">
    <div id="content-wrapper" class="d-flex flex-column">
      <div id="content">
        <Main/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import Main from './views/Main.vue';

export default defineComponent({
  name: 'App',
  components: {
    Main,
  },
});
</script>
