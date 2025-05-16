import type { RouteRecordRaw } from 'vue-router'
import SwitchboardPage from './pages/SwitchboardPage.vue'

export const switchboardRoutes: RouteRecordRaw[] = [
  {
    path: '/switchboard',
    name: 'Switchboard',
    component: SwitchboardPage,
  },
]
