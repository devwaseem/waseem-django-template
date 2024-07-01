import inject from '@rollup/plugin-inject';
import { glob } from 'glob';
import { resolve } from 'path';
import { defineConfig } from 'vite';

const dirs = ['assets', 'src'];

let inputFiles = [];

for (let dir of dirs) {
    const files = await glob(dir + '/**/*.{js,ts,css}', {
        ignore: ['node_modules/**', 'dist/**'],
    });
    inputFiles = [...inputFiles, ...files];
}

let rollupInput = {};

for (let file of inputFiles) {
    // let page_index = file.indexOf("pages");
    // let file_key = file.slice(page_index);
    rollupInput[file] = file;
}

export default defineConfig(({ mode }) => {
    return {
        root: '.',
        resolve: {
            alias: {
                '@assets': resolve('./assets'),
            },
        },
        server: {
            hmr: false,
        },
        build: {
            ssr: false,
            outDir: './dist', // puts the manifest.json in PROJECT_ROOT/build/static/ for Django to collect
            assetsDir: '',
            manifest: true, // adds a manifest.json
            emptyOutDir: true,
            sourcemap: mode == 'development' ? 'inline' : false,
            minify: mode == 'development' ? false : 'esbuild',
            rollupOptions: {
                output: {
                    compact: mode != 'development',
                    entryFileNames: '[name].[hash].js',
                    chunkFileNames: '[name].[hash].js',
                    assetFileNames: 'assets/[name].[hash][extname]',
                },
                input: rollupInput,
            },
        },
        plugins: [
            inject({
                htmx: 'htmx.org',
            }),
        ],
    };
});
