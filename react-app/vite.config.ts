import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  base: '/cses-analyses/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    fs: {
      allow: [
        // Allow serving markdown files from parent directory
        path.resolve(__dirname, '..'),
      ],
    },
  },
  assetsInclude: ['**/*.md'],
})
