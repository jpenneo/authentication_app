<template>
  <div class="login-container">
    <h1>Iniciar Sesión</h1>
    <form @submit.prevent="login">
      <label for="email">Correo Electrónico:</label>
      <input
        v-model="email"
        type="email"
        id="email"
        placeholder="Correo electrónico"
        required
      />

      <label for="password">Contraseña:</label>
      <input
        v-model="password"
        type="password"
        id="password"
        placeholder="Contraseña"
        required
      />

      <button type="submit" :disabled="loading">Iniciar Sesión</button>
    </form>
    <p v-if="error" class="error-message" v-text="error"></p>
  </div>
</template>

<script>
import DOMPurify from "dompurify";

import axios from "axios";
import { getCSRFToken, fetchCSRFToken } from "../utils/CSRF";

export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
      error: "",
      loading: false,
    };
  },
  methods: {
    sanitizeInput(input) {
      return DOMPurify.sanitize(input);
    },

    async login() {
      this.error = "";
      this.loading = true;

      try {
        // Obtener el token CSRF desde localStorage
        let csrfToken = getCSRFToken();
        if (!csrfToken) {
          // Si el token no está en localStorage, obtenerlo desde el servidor
          await fetchCSRFToken();
          csrfToken = getCSRFToken();

          if (!csrfToken) {
            this.error = "Token CSRF no encontrado.";
            return;
          }
        }

        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/inicio-sesion`,
          {
            email: this.sanitizeInput(this.email),
            password: this.sanitizeInput(this.password),
          },
          {
            headers: {
              "X-CSRFToken": csrfToken,
            },
            withCredentials: true, // Incluir cookies si es necesario
          }
        );

        // Almacenar el token CSRF y el token de autenticación
        const newCsrfToken = response.headers["x-csrftoken"];
        if (newCsrfToken) {
          localStorage.setItem("csrf_token", newCsrfToken);
        }

        const data = response.data;
        localStorage.setItem("token", data.token);
        this.$router.push("/dashboard");
      } catch (error) {
        this.error = error.response ? error.response.data.error : error.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped>
.login-container {
  background: rgb(211, 210, 210);
  color: black;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
}

form {
  font-weight: bold;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
}

input {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

p {
  color: red;
  text-align: center;
}
</style>
