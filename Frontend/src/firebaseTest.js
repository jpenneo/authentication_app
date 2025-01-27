import { getDatabase, ref, set, get } from "firebase/database";
import { initializeApp } from "firebase/app";

const firebaseConfig = {
    apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
    authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
    projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
    storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.VUE_APP_FIREBASE_APP_ID,
    measurementId: process.env.VUE_APP_FIREBASE_MEASUREMENT_ID
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Probar escritura y lectura
const testConnection = async () => {
  const testRef = ref(database, 'testConnection');
  try {
    await set(testRef, { status: 'connected' }); // Escribir un valor
    const snapshot = await get(testRef); // Leer el valor
    if (snapshot.exists()) {
      console.log('Conexión exitosa:', snapshot.val());
    } else {
      console.error('No se encontró el dato.');
    }
    
  } catch (error) {
    console.error('Error al probar la conexión:', error);
  }
};

testConnection();