import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import dotenv from "dotenv";
dotenv.config();

export default defineConfig({
  plugins: [react()],
  build: {
    sourcemap: true,
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_BE_URL,
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
