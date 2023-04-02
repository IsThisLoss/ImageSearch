<template>
  <div class="card shadow mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h6 class="center-text font-weight-bold">
          {{image.title}}
      </h6>
      <div class="float-right">
        <a class="btn" target="_blank" rel="nofollow" :href="image.url">
          <i class="fas fa-download"></i>
        </a>
        <a class="btn" target="_blank" rel="nofollow" @click="deleteImage">
          <i class="fas fa-trash-alt"></i>
        </a>
      </div>
    </div>
    <div class="card-body">
      <div class="text-center">
        <img
          class="img-fluid px-3 px-sm-4"
          style="width: 25rem;"
          :src="image.url"
          alt=""
        >
        <div>
          <p v-show="image.description.length > 0">
            {{image.description}}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { Image } from '@/api/images';

export default defineComponent({
  name: 'ImageCard',
  props: {
    image: {
      type: Object as PropType<Image>,
      required: true,
    },
  },
  methods: {
    deleteImage() {
      this.$emit('deleteImage', this.image.id)
    }
  }
});
</script>
