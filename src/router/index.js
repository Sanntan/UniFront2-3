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
    component: PersonalCabinet,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/') 
  } else {
    next()
  }
})

export default router