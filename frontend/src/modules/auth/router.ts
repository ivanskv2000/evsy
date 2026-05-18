import type { RouteRecordRaw } from 'vue-router'
import LoginPage from './pages/LoginPage.vue'
import SignupPage from './pages/SignupPage.vue'
import { useAppConfig } from '@/shared/composables/useAppConfig'

const { isDemo } = useAppConfig()

export const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  ...(!isDemo
    ? [
        {
          path: '/signup',
          name: 'Signup',
          component: SignupPage,
        },
      ]
    : []),
]
