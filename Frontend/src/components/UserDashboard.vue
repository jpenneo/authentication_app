<template>
  <div>
    <h1>Usuarios Registrados.</h1>
    <table>
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Correo Electrónico</th>
          <th>Contraseña</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.uid">
          <td v-text="sanitizeInput(user.user)"></td>
          <td v-text="sanitizeInput(user.email)"></td>
          <td v-text="user.password"></td>
        </tr>
      </tbody>
    </table>
    <p v-if="error" v-text="error" class="error-message"></p>
  </div>
</template>

<script>
import DOMPurify from "dompurify";

export default {
  data() {
    return {
      users: [], // Lista de usuarios obtenida del backend
      error: "", // Mensaje de error si ocurre un problema
    };
  },
  methods: {
    sanitizeInput(input) {
      return DOMPurify.sanitize(input); // Sanitizar las entradas de los usuarios
    },

    async fetchUsers() {
      try {
        // Obtener el token del almacenamiento local (guardado después del inicio de sesión)
        const token = localStorage.getItem("token");
        if (!token) {
          this.error = "No está autenticado. Por favor, inicie sesión.";
          this.$router.push("/inicio-sesion"); // Redirigir al inicio de sesión si no hay token
          return;
        }
        // Realizar la solicitud al backend para obtener los usuarios
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/auth/dashboard`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`, // Enviar el token en el encabezado de autorización
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error al obtener los datos.");
        }
        // Obtener los datos de los usuarios del backend
        const data = await response.json();
        this.users = data.users; // Asignar los datos a la lista de usuarios
      } catch (error) {
        this.error = error.message;
        console.error("Error al obtener los usuarios:", error);
      }
    },
  },
  created() {
    this.fetchUsers(); // Llamar a la función para obtener los usuarios al cargar el componente
  },
};
</script>

<style scoped>
table {
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
