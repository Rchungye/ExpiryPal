import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    sourcemap: true, // Habilitar mapas de origen
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001', // URL del backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
