import fs from 'node:fs';
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import tailwindcss from '@tailwindcss/vite';

function walk(dir) {
    const output = [];
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            output.push(...walk(full));
            continue;
        }
        output.push(full);
    }
    return output;
}

function discoverInputs(baseDirs) {
    const entries = {};
    for (const baseDir of baseDirs) {
        if (!fs.existsSync(baseDir)) {
            continue;
        }
        for (const file of walk(baseDir)) {
            const name = path.basename(file);
            const isEntry =
                name === 'entry.ts' ||
                name === 'entry.js' ||
                name === 'entry.head.ts' ||
                name === 'entry.head.js' ||
                name.endsWith('.entry.ts') ||
                name.endsWith('.entry.js');
            if (!isEntry) {
                continue;
            }

            const rel = path.relative(process.cwd(), file).replace(/\\/g, '/');
            entries[rel] = file;
        }
    }
    return entries;
}

export default defineConfig(async ({ mode }) => {
    const env = loadEnv(mode, process.cwd());
    const isDevelopment = mode == 'development';
    const outputDir = env.VITE_APP_OUTPUT_DIR || './dist';
    const hyperRoot = path.resolve('./hyper');
    const pageRoot = path.resolve('./hyper/pages');
    const routeRoot = path.resolve('./hyper/routes');
    const layoutRoot = path.resolve('./hyper/layouts');
    const sharedRoot = path.resolve('./hyper/shared');
    const inputs = discoverInputs([pageRoot, routeRoot, layoutRoot, sharedRoot]);

    return {
        root: '.',
        plugins: [
            tailwindcss(),
        ],
        resolve: {
            alias: {
                '@': hyperRoot,
                '@pages': pageRoot,
                '@routes': routeRoot,
                '@shared': sharedRoot,
                '@layouts': layoutRoot,
            },
        },
        build: {
            ssr: false,
            outDir: outputDir,
            manifest: true,
            emptyOutDir: true,
            sourcemap: isDevelopment ? 'inline' : false,
            minify: isDevelopment ? false : 'esbuild',
            rollupOptions: {
                input: inputs,
            },
        },
    };
});
