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
          <td v-text="maskedPassword(user.password)"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { collection, getDocs } from "firebase/firestore";
import { db } from "../firebase";
import DOMPurify from "dompurify";

export default {
  data() {
    return {
      users: [],
    };
  },
  methods: {
    sanitizeInput(input) {
      return DOMPurify.sanitize(input);
    },
    maskedPassword(password) {
      // Enmascarar la contraseña siempre que esté definida
      return "*".repeat(password.length);
    },
    async fetchUsers() {
      try {
        const querySnapshot = await getDocs(collection(db, "users"));
        this.users = querySnapshot.docs.map((doc) => {
          const data = doc.data();
          // Asegurarse de que los datos siempre tengan una contraseña
          if (!data.password) {
            throw new Error(
              `El documento con ID ${doc.id} no tiene una contraseña definida.`
            );
          }
          return { uid: doc.id, ...data };
        });
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
  },
  created() {
    this.fetchUsers();
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
</style>
