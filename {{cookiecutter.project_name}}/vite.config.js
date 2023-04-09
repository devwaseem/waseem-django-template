// const { resolve } = require('path');
// const fg = require('fast-glob');
// import { defineConfig } from 'vite';

import { resolve } from "path";
import { defineConfig, } from "vite";

const STATIC_SOURCE_DIR = "frontend/";

export default defineConfig({
        root: resolve(STATIC_SOURCE_DIR),
        base: "/static/", //same as `STATIC_URL` Django setting
        resolve: {
                alias: {
                        // Use '@' in urls as a shortcut for './static_source'.
                        "@": resolve(STATIC_SOURCE_DIR),
                        "@frontend": resolve(STATIC_SOURCE_DIR),
                },
        },
        server: {
                hmr: false,
        },
        build: {
                outDir: "./static", // puts the manifest.json in PROJECT_ROOT/static_source/ for Django to collect
                assetsDir: "",
                manifest: true, // adds a manifest.json
                emptyOutDir: true,
                rollupOptions: {
                        input: {
                                /* The bundle's entry point(s).  If you provide an array of entry points or an object mapping names to entry points, they will be bundled to separate output chunks. */
                                styles: resolve(__dirname, STATIC_SOURCE_DIR + "css/styles.js"),
                                // JS
                                main: resolve(__dirname, STATIC_SOURCE_DIR + "js/main.ts"),
                        },
                },
        },
        plugins: [
        ],
});
