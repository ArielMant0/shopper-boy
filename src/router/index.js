// Composables
import { createRouter, createWebHistory } from 'vue-router'

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
        component: () => import(/* webpackChunkName: "money" */ '@/views/Money.vue'),
      },
    ],
  }, {
    path: '/list',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'ShoppingList',
        component: () => import(/* webpackChunkName: "list" */ '@/views/ShoppingList.vue'),
      },
    ],
  }, {
    path: '/calendar',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Calendar',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Calendar.vue'),
      },
    ],
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
