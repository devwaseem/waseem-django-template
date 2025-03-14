/** @type {import('tailwindcss').Config} */

export default {
    content: [
      "./node_modules/flowbite/**/*.js",
      "./frontend/**/*.{html,js,ts,css,py}",
    ],
    theme: {
      extend: {},
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/container-queries'),
        require("flowbite/plugin"),
        plugin(function ({ addVariant }) {
            addVariant('htmx-settling', ['&.htmx-settling', '.htmx-settling &']);
            addVariant('htmx-request', ['&.htmx-request', '.htmx-request &']);
            addVariant('htmx-swapping', ['&.htmx-swapping', '.htmx-swapping &']);
            addVariant('htmx-added', ['&.htmx-added', '.htmx-added &']);
        }),
    ],
  };