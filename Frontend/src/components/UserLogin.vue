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

      <button type="submit">Iniciar Sesión</button>
    </form>
    <p v-if="error" v-text="error"></p>
  </div>
</template>

<script>
import { auth } from "../firebase";
import { signInWithEmailAndPassword } from "firebase/auth";
import DOMPurify from "dompurify";

export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
      error: "",
    };
  },
  methods: {
    sanitizeInput(input) {
      return DOMPurify.sanitize(input);
    },
    async login() {
      this.error = ""; // Reiniciar mensaje de error

      // Sanitizar los datos de entrada del usuario
      const sanitizedEmail = this.sanitizeInput(this.email);
      const sanitizedPassword = this.sanitizeInput(this.password);

      try {
        await signInWithEmailAndPassword(
          auth,
          sanitizedEmail,
          sanitizedPassword
        );
        this.$router.push("/dashboard");
      } catch (error) {
        if (error.code === "auth/user-not-found") {
          this.error = "Usuario no encontrado. Por favor, registre una cuenta.";
        } else if (error.code === "auth/wrong-password") {
          this.error = "Contraseña incorrecta. Por favor, intente de nuevo.";
        } else {
          this.error = this.sanitizeInput(error.message);
        }
      }
    },
  },
};
</script>

<style scoped>
.login-container {
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
