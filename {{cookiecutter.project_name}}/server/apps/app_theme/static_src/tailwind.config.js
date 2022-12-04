/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
const defaultTheme = require('tailwindcss/defaultTheme')
module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */
        '../../../../components/**/*.html',

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
        fontFamily: {
          sans: ["'Work Sans'", ...defaultTheme.fontFamily.sans]
        },
        colors: {
          background: "#F6F6F6",
          primary: {
            DEFAULT: '#222222',
            '50': '#7E7E7E',
            '100': '#747474',
            '200': '#5F5F5F',
            '300': '#4B4B4B',
            '400': '#363636',
            '500': '#222222',
            '600': '#060606',
            '700': '#000000',
            '800': '#000000',
            '900': '#000000'
          },
          accent: {
            DEFAULT: '#13C6FF',
            '50': '#CBF2FF',
            '100': '#B6EDFF',
            '200': '#8DE4FF',
            '300': '#65DAFF',
            '400': '#3CD0FF',
            '500': '#13C6FF',
            '600': '#00A5DA',
            '700': '#007BA2',
            '800': '#00506A',
            '900': '#002632'
          }
        },
        keyframes: {
          wiggle: {
            '0%, 100%': { transform: 'rotate(-3deg)' },
            '50%': { transform: 'rotate(3deg)' },
          },
          indeterminate: {
            '0%': {
              left: "-35%",
              right: "100%"
            },
            '60%': {
              left: "100%",
              right: "-90%"
            },
            '100%': {
              left: "100%",
              right: "-90%"
            },
          }
        },
        animation: {
          indeterminate: "indeterminate 2s cubic-bezier(0.65, 0.815, 0.735, 0.395) infinite"
        }
      },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
