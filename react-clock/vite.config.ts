import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

let hmr = {};
if (process.env.GITPOD_GIT_USER_EMAIL) {
  hmr = { port: 443 };
}

export default defineConfig({
  plugins: [react()],
  server: {
    hmr: hmr,
  },
})
