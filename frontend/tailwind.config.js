/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          primary: '#1f2937',
          secondary: '#374151',
          accent: '#4b5563',
          text: '#f3f4f6',
          muted: '#9ca3af'
        }
      }
    },
  },
  plugins: [],
}
