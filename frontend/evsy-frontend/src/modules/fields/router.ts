import type { RouteRecordRaw } from 'vue-router'
import FieldsPage from './pages/FieldsPage.vue'
import FieldDetailsPage from './pages/FieldDetailsPage.vue'
import FieldCreatePage from './pages/FieldCreatePage.vue'

export const fieldsRoutes: RouteRecordRaw[] = [
  {
    path: '/fields',
    name: 'Fields',
    component: FieldsPage,
  },
  {
    path: '/fields/new',
    name: 'NewField',
    component: FieldCreatePage,
  },
  {
    path: '/fields/:id',
    name: 'FieldDetails',
    component: FieldDetailsPage,
  },
]
