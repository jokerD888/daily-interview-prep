import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Vant from 'vant'
import 'vant/lib/index.css'
import './style.css'
import axios from 'axios'
import App from './App.vue'

const routes = [
  { path: '/', component: () => import('./views/Home.vue') },
  { path: '/login', component: () => import('./views/Login.vue') },
  { path: '/upload', component: () => import('./views/Upload.vue') },
  { path: '/review', component: () => import('./views/Review.vue') },
  { path: '/stats', component: () => import('./views/Stats.vue') },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (!token && to.path !== '/login') {
    return '/login'
  }
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
})
const app = createApp(App)
app.use(router)
app.use(Vant)
app.mount('#app')
