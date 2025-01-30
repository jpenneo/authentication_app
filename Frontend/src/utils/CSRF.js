import axios from "axios";

// Función para obtener el token CSRF desde el servidor
export const fetchCSRFToken = async () => {
  try {
    const response = await axios.get("/get-csrf-token");
    const token = response.data.csrf_token;
    if (token) {
      localStorage.setItem("csrf_token", token); // También puedes usar sessionStorage si prefieres
    }
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
  }
};

// Función para obtener el token CSRF desde localStorage o sessionStorage
export const getCSRFToken = () => {
  return localStorage.getItem("csrf_token"); // También puedes usar sessionStorage si prefieres
};

// Configurar Axios
export const configureAxios = () => {
  // Añadir un interceptor para incluir el token CSRF en las solicitudes
  axios.interceptors.request.use(
    (config) => {
      const token = getCSRFToken();
      if (token) {
        config.headers["X-CSRFToken"] = token;
      }
      config.withCredentials = true;
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
};

// Inicializar CSRF token al cargar la aplicación
export const initializeCSRF = async () => {
  await fetchCSRFToken();
  configureAxios();
};
