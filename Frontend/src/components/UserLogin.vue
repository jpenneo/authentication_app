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
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/auth/inicio-sesion`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: sanitizedEmail,
              password: sanitizedPassword,
            }),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error al iniciar sesión");
        }

        const data = await response.json();

        // Guardar el token en localStorage
        localStorage.setItem("token", data.token);

        // Guardar los datos del usuario o el token (si el backend lo envía)
        console.log(data);

        // Redirigir al dashboard
        this.$router.push("/dashboard");
      } catch (error) {
        this.error = error.message;
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
