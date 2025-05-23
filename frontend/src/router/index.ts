import { createRouter, createWebHistory } from 'vue-router'
import { fieldsRoutes } from '@/modules/fields/router'
import { eventsRoutes } from '@/modules/events/router'
import { tagsRoutes } from '@/modules/tags/router'
import { switchboardRoutes } from '@/modules/switchboard/router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/events' },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/shared/pages/NotFoundPage.vue'),
    },
    ...eventsRoutes,
    ...fieldsRoutes,
    ...tagsRoutes,
    ...switchboardRoutes,
  ],
})
