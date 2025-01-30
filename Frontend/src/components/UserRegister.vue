<template>
  <div class="register-container">
    <h1>Registro</h1>
    <form @submit.prevent="register">
      <label for="user">Usuario:</label>
      <input type="text" id="user" v-model="user" required />

      <label for="email">Correo Electrónico:</label>
      <input type="email" id="email" v-model="email" required />

      <label for="password">Contraseña:</label>
      <input
        type="password"
        id="password"
        v-model="password"
        @input="checkPasswordStrength"
        required
      />

      <div class="password-strength">
        <div
          class="strength-bar"
          :style="{
            width: passwordStrengthPercentage + '%',
            backgroundColor: passwordStrengthColor,
          }"
        ></div>
      </div>
      <p class="strength-label">{{ passwordStrengthLabel }}</p>

      <button type="submit" :disabled="loading">Registrarse</button>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { getCSRFToken } from "../utils/CSRF";

export default {
  data() {
    return {
      user: "",
      email: "",
      password: "",
      passwordStrengthPercentage: 0,
      passwordStrengthColor: "#e0e0e0",
      passwordStrengthLabel: "Débil",
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async register() {
      this.loading = true;
      this.errorMessage = "";

      try {
        const csrfToken = getCSRFToken(); // Obtener el token CSRF desde cookies/localStorage
        if (!csrfToken) {
          this.errorMessage =
            "Token CSRF no encontrado. Intenta recargar la página.";
          return;
        }

        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/registro`,
          {
            user: this.user,
            email: this.email,
            password: this.password,
          },
          {
            headers: {
              "X-CSRFToken": csrfToken,
            },
            withCredentials: true, // Incluir cookies si es necesario
          }
        );

        // Obtener el nuevo token CSRF si el backend lo envía
        const newCsrfToken = response.headers["x-csrftoken"];
        if (newCsrfToken) {
          localStorage.setItem("csrf_token", newCsrfToken);
        }

        alert("Registro exitoso. Ahora puedes iniciar sesión.");
        this.$router.push("/inicio-sesion");
      } catch (error) {
        this.errorMessage =
          error.response?.data?.error || "Error al registrar usuario.";
      } finally {
        this.loading = false;
      }
    },

    checkPasswordStrength() {
      const password = this.password;
      let strength = 0;

      if (password.length >= 8) strength += 25;
      if (/[A-Z]/.test(password)) strength += 25;
      if (/[a-z]/.test(password)) strength += 25;
      if (/\d/.test(password) || /[@$!%*?&]/.test(password)) strength += 25;

      this.passwordStrengthPercentage = strength;
      if (strength <= 25) {
        this.passwordStrengthColor = "red";
        this.passwordStrengthLabel = "Débil";
      } else if (strength <= 50) {
        this.passwordStrengthColor = "orange";
        this.passwordStrengthLabel = "Aceptable";
      } else if (strength <= 75) {
        this.passwordStrengthColor = "blue";
        this.passwordStrengthLabel = "Fuerte";
      } else {
        this.passwordStrengthColor = "green";
        this.passwordStrengthLabel = "Muy fuerte";
      }
    },
  },
};
</script>

<style scoped>
.register-container {
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

.password-strength {
  height: 10px;
  width: 100%;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
  margin: 5px 0;
}

.strength-bar {
  height: 100%;
  transition: width 0.3s, background-color 0.3s;
}

.strength-label {
  text-align: center;
  margin-top: 5px;
  font-size: 12px;
}

button {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: grey;
  cursor: not-allowed;
}

button:hover {
  background-color: #218838;
}

.error-message {
  color: red;
  font-size: 14px;
  text-align: center;
}
</style>
