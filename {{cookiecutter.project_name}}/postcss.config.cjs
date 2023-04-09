module.exports = {
    plugins: [
        require("tailwindcss/nesting"),
        require("tailwindcss"),
        require("autoprefixer"),
        require('postcss-import'),
        require('postcss-simple-vars'),
        require('postcss-nested'),
    ],
};
