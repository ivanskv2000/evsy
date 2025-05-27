import type { RouteRecordRaw } from 'vue-router'
import UserSettingsPage from './pages/UserSettingsPage.vue'

export const userRoutes: RouteRecordRaw[] = [
  {
    path: '/me',
    name: 'UserSettings',
    component: UserSettingsPage,
  }
]
