import type { RouteRecordRaw } from 'vue-router'
import LoginPage from './pages/LoginPage.vue'
import SignupPage from './pages/SignupPage.vue'

export const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupPage,
  },
]
