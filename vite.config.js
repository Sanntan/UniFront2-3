import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,                // вместо 'localhost', чтобы принимать внешние подключения
    open: true,
    allowedHosts: ['.ngrok-free.app']  // разрешаем все ngrok-домены
  }
})
