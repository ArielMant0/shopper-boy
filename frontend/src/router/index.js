// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Money from '@/views/Money.vue'
import Calendar from '@/views/Calendar.vue'
import Shopping from '@/views/Shopping.vue'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Money',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: Money,
      },
    ],
  }, {
    path: '/list',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Shopping',
        component: Shopping,
      },
    ],
  }, {
    path: '/calendar',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Calendar',
        component: Calendar,
      },
    ],
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
