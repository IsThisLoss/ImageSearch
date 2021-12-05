<template>
  <Header
    @searchSubmit="searchImage"
  />
  <div class="container-fluid">
    <h3 class="text-center my-4 text-gray-800">
        Images
    </h3>
    <div class="row">
        <div class="col-lg-4 mb-4">
          <NewImage
            @submit="createImage"
          />
        </div>
        <div
          v-for="image in images" :key="image.title"
          class="col-lg-4 mb-4"
        >
          <ImageCard
            :image="image"
            @deleteImage="deleteImage"
          />
        </div>
    </div>
  </div>
  <Footer/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import ImageCard from '@/components/ImageCard.vue';
import NewImage from '@/components/NewImage.vue';

import imagesApi, { InputImage, Image } from '@/api/images'

interface Data {
  images: Array<Image>
}

export default defineComponent({
  name: 'Main',
  components: {
    Header,
    Footer,
    ImageCard,
    NewImage,
  },
  data(): Data {
    return {
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
      })
      .catch(err => console.log(err))
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
