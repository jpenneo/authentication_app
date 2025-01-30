<template>
  <div>
    <h1>Usuarios Registrados.</h1>
    <table>
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Correo Electrónico</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.uid">
          <td v-text="sanitizeInput(user.user)"></td>
          <td v-text="sanitizeInput(user.email)"></td>
          <td>
            <button @click="viewUserDetails(user.uid)">Ver Detalles</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="error" v-text="error" class="error-message"></p>
  </div>
</template>

<script>
import DOMPurify from "dompurify";
import axios from "axios";
import { getCSRFToken, fetchCSRFToken } from "../utils/CSRF";

export default {
  data() {
    return {
      users: [],
      error: "",
    };
  },
  methods: {
    sanitizeInput(input) {
      return DOMPurify.sanitize(input);
    },

    async fetchUsers() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.error = "No está autenticado. Por favor, inicie sesión.";
          this.$router.push("/inicio-sesion");
          return;
        }

        // Obtener el token CSRF desde localStorage
        let csrfToken = getCSRFToken();
        if (!csrfToken) {
          // Si el token no está en localStorage, obtenerlo desde el servidor
          await fetchCSRFToken();
          csrfToken = getCSRFToken();

          if (!csrfToken) {
            this.error =
              "Token CSRF no encontrado. Por favor, recargue la página.";
            this.$router.push("/inicio-sesion");
            return;
          }
        }
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/auth/dashboard`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "X-CSRFToken": csrfToken,
            },
            withCredentials: true,
          }
        );

        // Obtener el nuevo token CSRF desde los encabezados de la respuesta
        const newCsrfToken = response.headers["x-csrftoken"];
        if (newCsrfToken) {
          localStorage.setItem("csrf_token", newCsrfToken); // Actualizar el token CSRF
        }

        this.users = response.data.users;
      } catch (error) {
        this.error = error.response ? error.response.data.error : error.message;
        console.error("Error al obtener los usuarios:", error);

        // Redirigir al inicio de sesión en caso de error de autenticación
        if (error.response && error.response.status === 401) {
          this.$router.push("/inicio-sesion");
        }
      }
    },

    viewUserDetails(uid) {
      console.log(`Ver detalles del usuario ${uid}`);
    },
  },
  created() {
    this.fetchUsers();
  },
};
</script>
<style scoped>
table {
  background: rgb(211, 210, 210);
  color: black;
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
  text-align: left;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 20px;
}
</style>
