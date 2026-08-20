import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    // Dev-time proxy so the frontend can call /api/... without hardcoding
    // http://localhost:5000 everywhere, and without needing CORS at all
    // in dev (Vite proxies same-origin). Flask's CORS config in
    // backend/app/config.py is still needed for any direct calls made
    // outside this proxy (e.g. a production build served separately).
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
