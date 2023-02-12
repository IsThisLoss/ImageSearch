<template>
<div class="container-fluid">
  <div class="card shadow-lg mt-5">
    <div class="card-header py-3">
      <h6 class="center-text font-weight-bold">
          Login
      </h6>
    </div>
    <div class="card-body p-0 p-5 text-center">
      <form @submit.prevent.stop="submit">
        <div class="form-group mt-2">
          <input
            type="text"
            class="form-control"
            placeholder="Username"
            v-model.trim="username"
          />
        </div>
        <div class="form-group mt-2">
          <input
            type="password"
            class="form-control"
            placeholder="Password"
            v-model.trim="password"
          />
        </div>
        <div
          v-show="error.length != 0"
          class="text-negative row justify-center text-h6"
        >
          {{ error }}
        </div>
        <button class="mt-2 btn btn-primary btn-block" type="submit">
          Login
        </button>
      </form>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import { auth, me } from '@/api/users'

export default defineComponent({
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      error: "",
    }
  },
  mounted() {
    me()
    .then(() => this.$router.push('/'))
    .catch(() => null)
  },
  methods: {
    submit() {
      auth(this.username, this.password).then(() => {
        this.$router.push('/')
      })
      .catch((err) => {
        const code = err.response.status
        if (code === 400 || code === 401) {
          this.error = "Incorrect password"
        } else {
          this.error = "Unexpected error"
        }
      })
    }
  },
})
</script>
