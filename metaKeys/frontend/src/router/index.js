import { createRouter, createWebHistory } from "vue-router";
import OwnersView from "../views/OwnersView.vue";
import GuestDashboard from "../views/GuestDashboard.vue";
import Login from '../views/Login.vue';

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/owners",
    name: "owners",
    component: OwnersView,
  },
  {
    path: "/guest",
    name: "GuestDashboard",
    component: GuestDashboard,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  if (to.name !== 'Login' && !isAuthenticated) next({ name: 'Login' });
  else next();
});

export default router;
