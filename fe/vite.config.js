import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import dotenv from "dotenv";

// Cargar variables de entorno
dotenv.config();

export default defineConfig({
  plugins: [react()],
  build: {
    sourcemap: true, // Habilitar mapas de origen
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_BE_URL, // Usar process.env aquí
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
