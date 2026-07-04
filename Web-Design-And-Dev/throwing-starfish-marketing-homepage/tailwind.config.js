/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Placeholder brand colors - update with actual brand colors when available
        'brand-primary': '#0066cc',
        'brand-secondary': '#ff6600',
        'brand-accent': '#00cc99',
        'brand-dark': '#333333',
        'brand-light': '#f5f5f5',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
} 