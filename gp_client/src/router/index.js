// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import GPHome from '../views/GPHome.vue'
import UserLogin from '../views/UserLogin.vue'
import UserRegister from '../views/UserRegister.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: GPHome
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/user-register',
    name: 'UserRegister',
    component: UserRegister
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
