import { createRouter, createWebHistory } from 'vue-router'
import { fieldsRoutes } from '@/modules/fields/router'
import { eventsRoutes } from '@/modules/events/router'
import { tagsRoutes } from '@/modules/tags/router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', redirect: '/events' }, ...eventsRoutes, ...fieldsRoutes, ...tagsRoutes],
})
