import { createRouter, createWebHistory } from 'vue-router';
import UserDashboard from '../components/UserDashboard.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';
import { auth } from '../firebase'; // Asegúrate de importar auth desde firebase.js

const routes = [
  {
    path: '/',
    redirect: '/inicio-sesion' // Redirige a la ruta de inicio de sesión
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/inicio-sesion',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/registro',
    name: 'UserRegister',
    component: UserRegister
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Agregar guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = auth.currentUser;
  if (requiresAuth && !isAuthenticated) {
    next('/inicio-sesion');
  } else {
    next();
  }
});

export default router;