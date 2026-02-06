export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['Fredoka', 'sans-serif'],
        body: ['Space Grotesk', 'sans-serif'],
      },
      colors: {
        ink: '#0b0f1a',
        glacier: '#dfe6f3',
        mist: '#a3b1c6',
        accent: '#a7f0ff',
        accent2: '#f7c7ff',
      }
    },
  },
  plugins: [],
}
