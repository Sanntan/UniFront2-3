import { createRouter, createWebHistory } from 'vue-router'
import MainContent from '../components/MainContent.vue'
import PersonalCabinet from '../components/PersonalCabinet.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainContent
  },
  {
    path: '/cabinet',
    name: 'PersonalCabinet',
    component: PersonalCabinet
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router