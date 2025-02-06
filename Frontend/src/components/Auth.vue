<template>
  <div>
    <h1>Login</h1>
    <input v-model="email" type="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Login</button>
    <button @click="register">Register</button>
    <p v-if="error" v-text="error"></p>
  </div>
</template>

<script>
import axios from "axios";
import { getCSRFToken, fetchCSRFToken } from "../utils/CSRF";

export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async login() {
      this.error = "";
      try {
        // Obtener el token CSRF desde localStorage
        let csrfToken = getCSRFToken();
        if (!csrfToken) {
          // Si el token no está en localStorage, obtenerlo desde el servidor
          await fetchCSRFToken();
          csrfToken = getCSRFToken();

          if (!csrfToken) {
            this.error = "Token CSRF no encontrado no tiene acceso.";
            return;
          }
        }

        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/inicio-sesion`,
          { email: this.email, password: this.password },
          {
            headers: { "X-CSRFToken": csrfToken },
            withCredentials: true,
          }
        );

        // Guardar token en localStorage si el backend lo devuelve
        if (response.data.token) {
          localStorage.setItem("token", response.data.token);
        }

        this.$router.push("/dashboard");
      } catch (error) {
        this.error = error.response?.data?.error || "Credenciales inválidas.";
      }
    },

    async register() {
      this.error = "";
      try {
        // Obtener el token CSRF desde localStorage
        let csrfToken = getCSRFToken();
        if (!csrfToken) {
          // Si el token no está en localStorage, obtenerlo desde el servidor
          await fetchCSRFToken();
          csrfToken = getCSRFToken();

          if (!csrfToken) {
            this.error = "Token CSRF no encontrado no tiene acceso.";
            return;
          }
        }

        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/registro`,
          { email: this.email, password: this.password },
          {
            headers: { "X-CSRFToken": csrfToken },
            withCredentials: true,
          }
        );

        if (response.data.token) {
          localStorage.setItem("token", response.data.token);
        }

        this.$router.push("/dashboard");
      } catch (error) {
        this.error = error.response?.data?.error || "Error al registrar.";
      }
    },
  },
};
</script>
