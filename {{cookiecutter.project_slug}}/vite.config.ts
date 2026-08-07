import fs from "node:fs";
import path from "node:path";

import tailwindcss from "@tailwindcss/vite";
import { defineConfig, loadEnv } from "vite";

function walk(directory: string): string[] {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

function discoverInputs(): Record<string, string> {
  const roots = ["hyper/layouts", "hyper/routes", "hyper/shared"];
  return roots
    .flatMap((root) => (fs.existsSync(root) ? walk(root) : []))
    .reduce(
      (inputs, file) => {
        const name = path.basename(file);
        if (name === "entry.ts" || name === "entry.head.ts") {
          inputs[path.relative(process.cwd(), file)] = file;
        }
        return inputs;
      },
      {} as Record<string, string>,
    );
}

export default defineConfig(({ mode }) => {
  const environment = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        "@shared": path.resolve("hyper/shared"),
        "@layouts": path.resolve("hyper/layouts"),
        "@routes": path.resolve("hyper/routes"),
      },
    },
    build: {
      manifest: true,
      outDir: environment.VITE_APP_OUTPUT_DIR || "dist",
      emptyOutDir: true,
      rollupOptions: { input: discoverInputs() },
    },
  };
});
