import axios from "axios";

// Función para obtener el token CSRF desde el servidor
export const fetchCSRFToken = async () => {
  try {
    const response = await axios.get(
      `${process.env.VUE_APP_API_URL}/get-csrf-token`
    );
    const token = response.data.csrf_token;
    if (token) {
      sessionStorage.setItem("csrf_token", token); // Se puede usar tanto sessionStorage como locaStorage.
    }
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
  }
};

// Función para obtener el token CSRF desde localStorage o sessionStorage
export const getCSRFToken = () => {
  return sessionStorage.getItem("csrf_token"); // Se puede usar tanto sessionStorage como locaStorage.
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
};
