import { createRouter, createWebHistory } from 'vue-router'; import
UserDashboard from '../components/UserDashboard.vue'; import UserLogin from
'../components/UserLogin.vue'; import UserRegister from
'../components/UserRegister.vue'; // Función para verificar la validez del token
JWT function isAuthenticated() { const token = localStorage.getItem('token'); //
Obtener el token del localStorage if (!token) return false; // Aquí podrías
agregar lógica para verificar si el token es válido, por ejemplo: try { const
decodedToken = JSON.parse(atob(token.split('.')[1])); // Decodificar el JWT (sin
verificar aún) const currentTime = Math.floor(Date.now() / 1000); // Tiempo
actual en segundos // Verifica si el token no ha expirado return
decodedToken.exp > currentTime; } catch (e) { return false; // Si no se puede
decodificar el token, no está autenticado } } const routes = [ { path: '/',
redirect: '/inicio-sesion' // Redirige a la ruta de inicio de sesión si no está
autenticado }, { path: '/dashboard', name: 'UserDashboard', component:
UserDashboard, meta: { requiresAuth: true } // Esta ruta requiere autenticación
}, { path: '/inicio-sesion', name: 'UserLogin', component: UserLogin }, { path:
'/registro', name: 'UserRegister', component: UserRegister } ]; const router =
createRouter({ history: createWebHistory(process.env.BASE_URL), routes }); //
Agregar guard de navegación para proteger rutas que requieren autenticación
router.beforeEach((to, from, next) => { const requiresAuth =
to.matched.some(record => record.meta.requiresAuth); // Verifica si la ruta
requiere autenticación const isAuthenticatedUser = isAuthenticated(); // Usar la
función para verificar si el usuario tiene un token válido if (requiresAuth &&
!isAuthenticatedUser) { next('/inicio-sesion'); // Redirige a login si no está
autenticado } else { next(); // Permite la navegación si el usuario está
autenticado } }); export default router;
