import inject from '@rollup/plugin-inject';
import { glob } from 'glob';
import { cpus } from 'os';
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import tailwindcss from 'tailwindcss';

const dirs = ['assets', 'app/templates'];

let inputFiles = [];

for (let dir of dirs) {
    const files = await glob(dir + '/**/*.{js,ts,css}', {
        ignore: ['node_modules/**', 'dist/**', '**/*.d.ts'],
    });
    inputFiles = [...inputFiles, ...files];
}

console.log(`Found ${inputFiles.length} files to build...`);

let rollupInput = {};

for (let file of inputFiles) {
    rollupInput[file] = file;
}

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd());
    const isDevelopment = mode == "development";
    const outputDir = env.VITE_APP_OUTPUT_DIR
    if (!outputDir) {
        throw Error('Set the output dir using {VITE_APP_OUTPUT_DIR} env variable')
    }
    return {
        root: '.',
        resolve: {
            alias: {
                '@assets': path.resolve('./assets'),
            },
        },
        server: {
            hmr: false,
        },
        css: {
            postcss: {
             plugins: [tailwindcss()],
            },
        },
        build: {
            ssr: false,
            outDir: outputDir,
            assetsDir: '',
            manifest: true,
            emptyOutDir: true,
            sourcemap: isDevelopment ? 'inline' : false,
            minify: isDevelopment ? false : 'esbuild',
            rollupOptions: {
                maxParallelFileOps: Math.max(1, cpus().length - 1),
                output: {
                    compact: isDevelopment,
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
