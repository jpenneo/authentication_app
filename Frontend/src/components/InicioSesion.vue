<template>
  <div>
    <h1>Iniciar sesión</h1>
    <form @submit.prevent="loginUser">
      <input v-model="user" placeholder="Usuario" type="user" />
      <input
        v-model="email"
        placeholder="Correo electrónico"
        type="email"
        required
      />
      <input
        v-model="password"
        placeholder="Contraseña"
        type="password"
        required
      />
      <button type="submit">Ingresar</button>
      <!-- Mostrar mensaje de error si existe -->
      <p v-if="errorMessage" class="error" v-text="errorMessage"></p>
    </form>
  </div>
</template>

<script>
import { auth } from "@/firebase"; // Asegúrate de que la configuración de Firebase esté correcta
import { signInWithEmailAndPassword } from "firebase/auth";
import DOMPurify from "dompurify";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "", // Variable para mostrar mensajes de error
    };
  },
  methods: {
    sanitizeInput(input) {
      return DOMPurify.sanitize(input);
    },
    async loginUser() {
      this.errorMessage = ""; // Reiniciar mensaje de error
      const sanitizedEmail = this.sanitizeInput(this.email);
      const sanitizedPassword = this.sanitizeInput(this.password);

      try {
        const userCredential = await signInWithEmailAndPassword(
          auth,
          sanitizedEmail,
          sanitizedPassword
        );
        console.log("Usuario autenticado:", userCredential.user);

        // Redirigir a una página después de iniciar sesión
        this.$router.push("/");
      } catch (error) {
        console.error("Error al iniciar sesión:", error.message);
        // Mostrar el mensaje de error al usuario
        this.errorMessage =
          "Error al iniciar sesión. Verifica tus credenciales.";
      }
    },
  },
};
</script>

<style scoped>
/* Estilos básicos para el formulario */
form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: 0 auto;
}

input {
  margin: 10px 0;
  padding: 10px;
  font-size: 1rem;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 1rem;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  font-size: 0.9rem;
  margin-top: 10px;
}
</style>
