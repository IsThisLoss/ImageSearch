<template>
  <div class="card shadow mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h6 class="center-text font-weight-bold">
          {{image.title}}
      </h6>
      <div class="float-right">
        <a class="btn btn-light" role="button" @click="copyToClipboard(image.links.orig)">
          <i class="fas fa-clipboard" aria-hidden="true"></i>
        </a>
        <a class="btn btn-light" role="button" target="_blank" rel="nofollow" :href="image.links.orig">
          <i class="fas fa-download"></i>
        </a>
        <a class="btn btn-light" role="button" @click="deleteImage">
          <i class="fas fa-trash-alt"></i>
        </a>
      </div>
    </div>
    <div class="card-body">
      <div class="text-center">
        <img
          class="img-fluid px-3 px-sm-4"
          style="width: 25rem;"
          :src="image.links.previews.medium"
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
    },
    copyToClipboard(link: string) {
      if (!link.startsWith('http')) {
        link = location.host + link
      }
      navigator.clipboard.writeText(link)
    }
  },
});
</script>
