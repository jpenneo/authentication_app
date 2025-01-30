<template>
  <div>
    <header>
      <nav>
        <router-link to="/registro">Registro</router-link>
        <router-link to="/inicio-sesion">Iniciar sesión</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>Derechos reservados &copy; 2025</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
  methods: {
    sanitizeRoute(route) {
      // Sanitizar las rutas usando encodeURI para evitar inyección de código
      return encodeURI(route);
    },
  },
};
</script>

<style scoped>
header {
  background-color: #efe8d5;
  color: blue;
  text-align: center;
  margin: 0;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  padding: 1em 0;
}

/* Contenido principal */
main {
  background-color: #ecd5f0;
  color: blue;
  font-size: medium;
  padding: 2em;
}
nav {
  display: flex;
  gap: 10px;
}
footer {
  background-color: #5e5c5c; /* Fondo oscuro */
  color: rgb(255, 255, 255);
  padding: 10px;
  text-align: center;
}
</style>
