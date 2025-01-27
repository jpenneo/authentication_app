<template>
  <div>
    <nav>
      <router-link to="/registro">Registro</router-link> 
      <router-link to="/inicio-sesion">Iniciar sesión</router-link> 
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    sanitizeRoute(route) {
      // Sanitizar las rutas usando encodeURI para evitar inyección de código
      return encodeURI(route);
    }
  }
};
</script>

<style scoped>
nav {
  display: flex;
  gap: 10px;
}
</style>
