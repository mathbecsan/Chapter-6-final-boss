import { defineConfig } from 'vite';
import { viteSingleFile } from 'vite-plugin-singlefile';

// Builds the whole game (code + spritesheets + music) into ONE html file:
//   npx vite build --config vite.standalone.config.js
export default defineConfig({
  plugins: [viteSingleFile()],
  build: {
    assetsInlineLimit: 100000000,
    chunkSizeWarningLimit: 100000000,
    outDir: 'dist-standalone',
    rollupOptions: { input: 'index-standalone.html' },
  },
});
