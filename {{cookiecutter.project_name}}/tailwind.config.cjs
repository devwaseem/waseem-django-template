/** @type {import('tailwindcss').Config} */

export default {
    content: [
      "./hyper/**/*.{html,js,ts,css,py}",
    ],
    theme: {
      extend: {},
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
    ],
  };
