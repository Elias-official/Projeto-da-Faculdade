export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      boxShadow: {
        soft: '0 20px 60px rgba(15, 23, 42, 0.25)',
        glow: '0 0 35px rgba(37, 99, 235, 0.14)',
      },
      backgroundImage: {
        'futuristic-gradient': 'radial-gradient(circle at top, rgba(59,130,246,0.18), transparent 35%)',
      },
    },
  },
  plugins: [],
}
