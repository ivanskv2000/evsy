import type { RouteRecordRaw } from 'vue-router'
import EventsPage from './pages/EventsPage.vue'

export const eventsRoutes: RouteRecordRaw[] = [
  {
    path: '/events',
    name: 'Events',
    component: EventsPage,
  },
  {
    path: '/events/new',
    name: 'NewEvent',
    component: EventsPage,
  },
]
