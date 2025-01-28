<template>
  <div class="register-container">
    <h1>Registro</h1>
    <form @submit.prevent="register">
      <label for="user">Usuario:</label>
      <input
        v-model="user"
        type="text"
        id="user"
        placeholder="Usuario"
        required
        autocomplete="username"
      />

      <label for="email">Correo Electrónico:</label>
      <input
        v-model="email"
        type="email"
        id="email"
        placeholder="Correo electrónico"
        required
        autocomplete="email"
      />

      <label for="password">Contraseña:</label>
      <input
        v-model="password"
        type="password"
        id="password"
        placeholder="Contraseña"
        required
        autocomplete="new-password"
        @input="checkPasswordStrength"
      />
      <!-- Indicador de fortaleza de contraseña -->
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

      <button type="submit" :disabled="passwordStrength < 3">Registrar</button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: "UserRegister",
  data() {
    return {
      user: "",
      email: "",
      password: "",
      error: "",
      passwordStrength: 0, // Nivel de fortaleza de la contraseña (0-5)
      passwordStrengthColor: "black", // Color del indicador
      passwordStrengthLabel: "", // Etiqueta descriptiva
    };
  },
  methods: {
    checkPasswordStrength() {
      let strength = 0;
      const length = this.password.length;

      // Incrementar fortaleza según los criterios
      if (length >= 8) strength++; // Longitud mínima
      if (length >= 10) strength++; // Longitud aceptable
      if (/[A-Z]/.test(this.password)) strength++; // Contiene mayúsculas
      if (/[a-z]/.test(this.password)) strength++; // Contiene minúsculas
      if (/\d/.test(this.password)) strength++; // Contiene números
      if (/[@$!%*?&]/.test(this.password)) strength++; // Contiene caracteres especiales

      // Actualizar propiedades de visualización
      this.passwordStrength = strength;
      this.updateStrengthVisuals(strength);
    },
    updateStrengthVisuals(strength) {
      // Asignar color y descripción según la fortaleza
      if (strength < 3) {
        this.passwordStrengthColor = "red";
        this.passwordStrengthLabel = "Débil";
      } else if (strength === 3) {
        this.passwordStrengthColor = "orange";
        this.passwordStrengthLabel = "Aceptable";
      } else if (strength === 4) {
        this.passwordStrengthColor = "yellow";
        this.passwordStrengthLabel = "Buena";
      } else if (strength >= 5) {
        this.passwordStrengthColor = "green";
        this.passwordStrengthLabel = "Muy Fuerte";
      }
    },
    async register() {
      if (this.passwordStrength < 3) {
        this.error = "La contraseña no cumple con los requisitos mínimos.";
        return;
      }

      try {
        // Realizar la solicitud al backend para registrar al usuario
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/auth/register`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user: this.user,
              email: this.email,
              password: this.password,
            }),
          }
        );

        // Comprobar la respuesta del servidor
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error al registrar el usuario.");
        }

        // Si la respuesta es exitosa, redirigir al inicio de sesión
        this.$router.push("/inicio-sesion");
      } catch (error) {
        this.error = error.message;
        console.error("Error al registrar el usuario:", error);
      }
    },
  },
};
</script>

<style scoped>
.register-container {
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
