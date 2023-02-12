<template>
<div class="card shadow-lg">
  <div class="card-header py-3">
    <h6 class="center-text font-weight-bold">
        Add new image
    </h6>
  </div>
  <div class="card-body p-0">
    <div class="p-5">
      <div class="text-center">
        <h4 class="text-gray-900 mb-4">
            New image
        </h4>
        <form @submit.prevent.stop="submit">
          <div class="form-group mt-2">
            <input
              type="text"
              class="form-control"
              placeholder="Title"
              v-model.trim="title"
            />
          </div>
          <div class="form-group mt-2">
            <input
              type="text"
              class="form-control"
              placeholder="Description"
              v-model.trim="description"
            />
          </div>
          <!--
          <div class="form-group mt-2">
            <input
              type="text"
              class="form-control"
              placeholder="URL"
              v-model.trim="url"
            />
          </div>
          -->
          <input
            v-on:change="handleFileUpload($event)"
            type="file"
            class="mt-2 form-control"
            ref="fileInput"
            accept=".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|image/*"
          >
          <button class="mt-2 btn btn-primary btn-block" type="submit">
              Save
          </button>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { InputImage } from '@/api/images'
import mediaApi from '@/api/media'

export default defineComponent({
  data(): InputImage {
    return {
      title: "",
      description: "",
      url: "",
    }
  },
  methods: {
    submit() {
      if (!this.isValid()) {
        return
      }
      const image = {
        title: this.title,
        description: this.description,
        url: this.url,
      }
      this.$emit('submit', image);
      this.clear()
    },
    clear() {
      this.title = ""
      this.description = ""
      this.url = ""
      const fileInput = this.$refs.fileInput as any
      fileInput.value = null
    },
    isValid(): boolean {
      if (this.title === "" || this.description == "" || this.url === "") {
        return false
      }
      return true
    },
    handleFileUpload(event: any) {
      const file = event.target.files[0];
      const data = new FormData();
      data.append('file', file, file.name);
      mediaApi.upload(data).then((resp: string) => {
        this.url = resp
      })
    },
  },
})
</script>
