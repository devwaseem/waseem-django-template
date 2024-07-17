/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');
const { spawnSync } = require('child_process');
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
    content: [
        '!./node_modules/',
        '!./dist/',
        './node_modules/flowbite/**/*.js',
        './**/*.html',
        './**/*.js',
        './**/*.ts',
        './**/*.py',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: [...defaultTheme.fontFamily.sans],
                'serif-text': [...defaultTheme.fontFamily.serif],
                'serif-display': [...defaultTheme.fontFamily.serif],
                mono: [...defaultTheme.fontFamily.mono],
            },
            colors: {
                primary: {
                    DEFAULT: '#6c5be5',
                    50: '#f4f2ff',
                    100: '#eae8ff',
                    200: '#d8d4ff',
                    300: '#bab2ff',
                    400: '#9e8dff',
                    500: '#7755fd',
                    600: '#6632f5',
                    700: '#5720e1',
                    800: '#491abd',
                    900: '#3e189a',
                },
            },
            keyframes: {
                shake: {
                    '10%, 90%': {
                        transform: 'translate3d(-1px, 0, 0)',
                    },
                    '20%, 80%': {
                        transform: 'translate3d(2px, 0, 0)',
                    },
                    '30%, 50%, 70%': {
                        transform: 'translate3d(-4px, 0, 0)',
                    },
                    '40%, 60%': {
                        transform: 'translate3d(4px, 0, 0)',
                    },
                },
                wiggle: {
                    '0%, 100%': { transform: 'rotate(-3deg)' },
                    '50%': { transform: 'rotate(3deg)' },
                },
                indeterminate: {
                    '0%': {
                        left: '-35%',
                        right: '100%',
                    },
                    '60%': {
                        left: '100%',
                        right: '-90%',
                    },
                    '100%': {
                        left: '100%',
                        right: '-90%',
                    },
                },
            },
            animation: {
                indeterminate: 'indeterminate 2s cubic-bezier(0.65, 0.815, 0.735, 0.395) infinite',
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/container-queries'),
        require('flowbite/plugin'),
        plugin(function ({ addVariant }) {
            addVariant('htmx-settling', ['&.htmx-settling', '.htmx-settling &']);
            addVariant('htmx-request', ['&.htmx-request', '.htmx-request &']);
            addVariant('htmx-swapping', ['&.htmx-swapping', '.htmx-swapping &']);
            addVariant('htmx-added', ['&.htmx-added', '.htmx-added &']);
        }),
    ],
};
