import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/tests/setup-vitest.ts',
    include: ['**/*.test.{ts,tsx}'], // Solo tests unitarios (.test.ts/.test.tsx)
    exclude: ['**/node_modules/**', '**/*.spec.ts'], // Excluir E2E (.spec.ts)
    coverage: {
      reporter: ['text', 'html'],
      exclude: [
        'node_modules/',
        'src/tests/**/*.spec.ts', // Excluir E2E del coverage
        '**/*.config.{js,ts}',
        '**/**.d.ts',
      ],
    },
  },
});
