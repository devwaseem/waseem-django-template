module.exports = {
  printWidth: 120,
  tabWidth: 4,
  useTabs: false,
  semi: true,
  singleQuote: true,
  trailingComma: "es5",
  bracketSpacing: true,
  arrowParens: "always",
  requirePragma: false,
  proseWrap: "preserve",
  plugins: [
    "prettier-plugin-organize-imports",
    require("prettier-plugin-tailwindcss"),
  ],
  tailwindConfig: "./tailwind.config.cjs",
};
