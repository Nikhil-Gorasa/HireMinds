import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import CVUpload from './components/CVUpload.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/cv-analysis',
    name: 'CVAnalysis',
    component: CVUpload
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 