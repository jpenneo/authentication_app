<template>
  <div class="register-container">
    <h1>Registro</h1>
    <form @submit.prevent="register">
      <label for="user">Usuario:</label>
      <input
        v-model="user"
        type="user"
        id="user"
        placeholder="Usuario"
        required
        autocomplete="user"
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
      />

      <button type="submit">Registrar</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import { auth, db } from "../firebase";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { setDoc, doc } from "firebase/firestore";

export default {
  name: "UserRegister",
  data() {
    return {
      user: "",
      email: "",
      password: "",
      error: "",
    };
  },
  methods: {
    validatePassword(password) {
      // La contraseña debe tener al menos 8 caracteres, una minúscula, una mayúscula, un número y un carácter especial
      const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return regex.test(password);
    },
    async register() {
      if (!this.validatePassword(this.password)) {
        this.error =
          "La contraseña debe tener al menos 8 caracteres, una minúscula, una mayúscula, un número y un carácter especial.";
        return;
      }
      try {
        const userCredential = await createUserWithEmailAndPassword(
          auth,
          this.email,
          this.password
        );
        const user = userCredential.user;
        // No almacenes la contraseña en texto plano en una aplicación real
        await setDoc(doc(db, "users", user.uid), {
          user: this.user,
          email: this.email,
          password: this.password,
        });
        this.$router.push("/inicio-sesion");
      } catch (error) {
        this.error = error.message;
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

button {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

p {
  color: red;
  text-align: center;
}
</style>
