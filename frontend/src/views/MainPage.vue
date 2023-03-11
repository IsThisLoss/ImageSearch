<template>
<div v-show="loaded">
  <PageHeader
    @searchSubmit="searchImages"
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
  <div id="page-bottom"/>
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
  offset: number
  hasMoreImages: boolean
  loadingNextPage: boolean
  text?: string
}

const LIMIT = 5

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
      offset: 0,
      hasMoreImages: true,
      loadingNextPage: false,
      text: undefined,
    }
  },
  mounted() {
    window.onscroll = () => {
      const scrolledTo = document.querySelector('#page-bottom')
      if (scrolledTo && this.isScrolledIntoView(scrolledTo)) {
        this.loadNextPage()
      }
    }
    this.reloadImages()
  },
  methods: {
    reloadImages() {
      this.searchImages()
    },
    searchImages(text?: string) {
      this.text = text
      this.offset = 0
      this.hasMoreImages = true

      imagesApi.find(this.offset, LIMIT, this.text)
      .then(resp => {
        this.images = resp.images
        this.loaded = true
      })
      .catch(this.handleError)
    },
    loadNextPage() {
      if (!this.hasMoreImages || this.loadingNextPage) {
        return
      }
      this.loadingNextPage = true
      this.offset += LIMIT
      imagesApi.find(this.offset, LIMIT, this.text)
      .then(resp => {
        this.loadingNextPage = false
        if (resp.images.length === 0) {
          this.hasMoreImages = false
          return
        }
        this.images = this.images.concat(resp.images)
      })
      .catch(this.handleError)
    },
    createImage(image: InputImage) {
      imagesApi.create(image)
      .then(_ => this.reloadImages())
      .catch(this.handleError)
    },
    deleteImage(id: string) {
      imagesApi.delete(id)
      .then(_ => this.reloadImages())
      .catch(this.handleError)
    },
    handleError(err: any) {
      const code = err.response.status
      if (code === 401) {
        this.$router.push('/login')
      }
    },
    isScrolledIntoView(el: any) {
      const rect = el.getBoundingClientRect()
      const elemTop = rect.top
      const elemBottom = rect.bottom

      const isVisible = elemTop < window.innerHeight && elemBottom >= 0
      return isVisible
    },
  },
});
</script>
