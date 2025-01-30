import axios from "axios";

// Función para obtener el token CSRF desde la cookie o del header
export const getCSRFToken = () => {
  return document.cookie
    .split(";")
    .find((cookie) => cookie.trim().startsWith("csrf_token="))
    ?.split("=")[1]; // Asume que el token está en una cookie llamada csrf_token
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
