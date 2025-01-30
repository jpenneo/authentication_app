import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import { configureAxios } from "./utils/CSRF";

// Configurar Axios
configureAxios();

// Crear la aplicación Vue
const app = createApp(App);

// Usar el enrutador en la aplicación
app.use(router);

// Validar el elemento de montaje
const mountElement = document.getElementById("app");
if (mountElement) {
  // Montar la aplicación en el elemento del DOM con ID 'app'
  app.mount("#app");
} else {
  console.error("El elemento de montaje no se encontró en el DOM.");
}
