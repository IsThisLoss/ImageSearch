<template>
<div v-show="loaded">
  <PageHeader
    @searchSubmit="searchImage"
  />
  <div class="container-fluid">
    <h3 class="text-center my-4 text-gray-800">
        Images
    </h3>
    <div class="row">
      <div class="col-lg-4 mb-4">
        <NewImage @submit="createImage"/>
      </div>
      <div
        v-for="image in images" :key="image.title"
        class="col-lg-4 mb-4"
      >
        <ImageCard :image="image" @deleteImage="deleteImage"/>
      </div>
    </div>
  </div>
  <PageFooter/>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import PageHeader from '@/components/PageHeader.vue';
import PageFooter from '@/components/PageFooter.vue';
import ImageCard from '@/components/ImageCard.vue';
import NewImage from '@/components/NewImage.vue';

import imagesApi, { InputImage, Image } from '@/api/images'

interface Data {
  loaded: boolean
  images: Array<Image>
}

export default defineComponent({
  name: 'MainPage',
  components: {
    PageHeader,
    PageFooter,
    ImageCard,
    NewImage,
  },
  data(): Data {
    return {
      loaded: false,
      images: [],
    }
  },
  mounted() {
    this.getAllImages()
  },
  methods: {
    getAllImages() {
      imagesApi.getAll()
      .then(resp => {
        this.images = resp.images
        this.loaded = true
      })
      .catch((err) => {
        console.log(err)
        const code = err.response.status
        if (code === 401) {
          this.$router.push('/login')
        }
      })
    },
    createImage(image: InputImage) {
      imagesApi.create(image)
      .then(_ => this.getAllImages())
      .catch(err => console.log(err))
    },
    searchImage(text: string) {
      if (text === "") {
        this.getAllImages()
        return
      }
      imagesApi.search(text)
      .then(resp => {
        this.images = resp.images
      })
      .catch(err => console.log(err))
    },
    deleteImage(id: string) {
      imagesApi.delete(id)
      .then(_ => this.getAllImages())
      .catch(err => console.log(err))
    },
  },
});
</script>
