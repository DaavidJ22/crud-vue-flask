import { createRouter, createWebHistory } from 'vue-router'
import ClientesView from '../views/ClientesView.vue'
import DashboardView from '../views/DashboardView.vue'
import PedidosView from '../views/PedidosView.vue'
import ProductosView from '../views/ProductosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/clientes',
      name: 'clientes',
      component: ClientesView,
    },
    {
      path: '/productos',
      name: 'productos',
      component: ProductosView,
    },
    {
      path: '/pedidos',
      name: 'pedidos',
      component: PedidosView,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard',
    },
  ],
})

export default router
