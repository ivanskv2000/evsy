import type { RouteRecordRaw } from 'vue-router'
import TagsPage from './pages/TagsPage.vue'
import TagCreatePage from './pages/TagCreatePage.vue'

export const tagsRoutes: RouteRecordRaw[] = [
  {
    path: '/tags',
    name: 'Tags',
    component: TagsPage,
  },
  {
    path: '/tags/new',
    name: 'NewTag',
    component: TagCreatePage,
  },
  {
    path: '/tags/:id',
    name: 'TagDetails',
    component: TagsPage,
  },
]
