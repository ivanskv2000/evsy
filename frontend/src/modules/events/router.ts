import type { RouteRecordRaw } from 'vue-router'
import EventsPage from './pages/EventsPage.vue'
import EventDetailsPage from './pages/EventDetailsPage.vue'
import EventCreatePage from './pages/EventCreatePage.vue'

export const eventsRoutes: RouteRecordRaw[] = [
  {
    path: '/events',
    name: 'Events',
    component: EventsPage,
  },
  {
    path: '/events/new',
    name: 'NewEvent',
    component: EventCreatePage,
  },
  {
    path: '/events/:id',
    name: 'EventDetails',
    component: EventDetailsPage,
  },
]
