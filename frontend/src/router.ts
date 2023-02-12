import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import MainPage from './views/MainPage.vue'
import LoginPage from './views/LoginPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Main',
    component: MainPage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
]

const router = createRouter({
   history: createWebHistory(process.env.BASE_URL),
   routes,
})

export default router
