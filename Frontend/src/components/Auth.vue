<template>
  <div>
    <h1>Login</h1>
    <input v-model="user" type="user" placeholder="User" />
    <input v-model="email" type="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Login</button>
    <button @click="register">Register</button>
    <p v-if="error" v-text="error"></p>
  </div>
</template>

<script>
import { auth } from "../firebase";
import DOMPurify from "dompurify";

export default {
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
      const sanitizedEmail = this.sanitizeInput(this.email);
      const sanitizedPassword = this.sanitizeInput(this.password);
      try {
        await auth.signInWithEmailAndPassword(
          sanitizedEmail,
          sanitizedPassword
        );
        this.$router.push("/");
      } catch (error) {
        this.error = this.sanitizeInput(error.message);
      }
    },
    async register() {
      const sanitizedEmail = this.sanitizeInput(this.email);
      const sanitizedPassword = this.sanitizeInput(this.password);
      try {
        await auth.createUserWithEmailAndPassword(
          sanitizedEmail,
          sanitizedPassword
        );
        this.$router.push("/");
      } catch (error) {
        this.error = this.sanitizeInput(error.message);
      }
    },
  },
};
</script>
