/// <reference types="vitest" />

import path from 'node:path'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [vue(), tailwindcss()],

  server: {
    host: true,
    port: 5173,
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  test: {
    globals: true,
    environment: 'jsdom',
  },

  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          tanstack: ['@tanstack/vue-table'],
          veevalidate: ['vee-validate'],
          ui: ['reka-ui'],
          sonner: ['vue-sonner'],
          zod: ['zod'],
        },
      },
    },
  },

  optimizeDeps: {
    exclude: ['@tanstack/vue-table', 'vee-validate', 'reka-ui', 'vue-sonner', 'zod'],
  },
})
