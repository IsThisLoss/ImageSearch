<template>
<div class="card shadow mb-4">
  <div class="card-header py-3">
    <h6 class="center-text font-weight-bold">
        Add new image
    </h6>
  </div>
  <div class="card-body p-5">
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
              v-model.trim="image.title"
            />
          </div>
          <div class="form-group mt-2">
            <input
              type="text"
              class="form-control"
              placeholder="Description"
              v-model.trim="image.description"
            />
          </div>
          <input
            v-on:change="handleFileUpload($event)"
            type="file"
            class="mt-2 form-control"
            ref="fileInput"
            accept=".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|image/*"
          >
          <button :disabled="isSubmitDisabled" class="mt-2 btn btn-primary" type="submit">
              {{buttonText}}
          </button>
        </form>
      </div>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { InputImage } from '@/api/images'
import mediaApi from '@/api/media'

interface Data {
  image: InputImage
  buttonText: string
}

const DEFAULT_BUTTON_TEXT = "Save"
const UPLOADING_BUTTON_TEXT = "Uploading..."

export default defineComponent({
  data(): Data {
    return {
      image: {
        title: "",
        description: "",
        url: "",
      },
      buttonText: DEFAULT_BUTTON_TEXT,
    }
  },
  methods: {
    submit() {
      const image = {
        title: this.image.title,
        description: this.image.description,
        url: this.image.url,
      }
      this.$emit('submit', image);
      this.clear()
    },
    clear() {
      this.image.title = ""
      this.image.description = ""
      this.image.url = ""
      const fileInput = this.$refs.fileInput as any
      fileInput.value = null
    },
    handleFileUpload(event: any) {
      this.buttonText = UPLOADING_BUTTON_TEXT
      const file = event.target.files[0];
      const data = new FormData();
      data.append('file', file, file.name);
      mediaApi.upload(data).then((resp: string) => {
        this.image.url = resp
        this.buttonText = DEFAULT_BUTTON_TEXT
      })
    },
  },
  computed: {
    isSubmitDisabled(): boolean {
      if (this.image.title === "" || this.image.url === "") {
        return true
      }
      return false
    }
  },
})
</script>
