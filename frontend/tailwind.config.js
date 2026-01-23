/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ea580c', // Orange-600
        secondary: '#1f2937', // Gray-800
        dark: '#121212',
      }
    },
  },
  plugins: [],
}