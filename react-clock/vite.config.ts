import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

let server = 'ws://localhost:8080';
if (process.env.GITPOD_GIT_USER_EMAIL) {
  server = server = `ws://${process.env.GITPOD_WORKSPACE_ID}.${process.env.GITPOD_WORKSPACE_CLUSTER_HOST}`
}



export default defineConfig({
  plugins: [react()],
  
  define: {
    __APP_BACKEND__: JSON.stringify(server),
  },
})
