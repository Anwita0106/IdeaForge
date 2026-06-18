import { defineConfig } from 'vite';

// Minimal config: Vite just serves/builds the existing index.html as-is.
// No framework plugins are needed since the UI is plain HTML/CSS/JS.
// VITE_API_BASE_URL (from .env / .env.production) is substituted directly
// into index.html via Vite's built-in %VAR_NAME% HTML replacement - see the
// <script> tag near the top of the body in index.html.
export default defineConfig({
  server: {
    port: 5173,
  },
  preview: {
    port: 4173,
  },
});
