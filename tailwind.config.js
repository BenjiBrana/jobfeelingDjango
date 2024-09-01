/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,ts,jsx,tsx,mdx,py}', // Inclut tous les fichiers pertinents dans src
    './templates/**/*.html',                  // Inclut les fichiers HTML dans templates
    './static/**/*.css'                       // Inclut les fichiers CSS dans static
  ],
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 1s ease forwards',
        'fade-out': 'fadeOut 0.5s ease forwards',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-out': {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
      },
      screens: {
        'tablette': { 'max': '1023px' },
        'mobile': { 'max': '639px' },
      },
      spacing: {
        128: '32rem',
      },
      colors: {
        background: '#F4F4F4',
        backgroundDark: '#0A0A0A',
        secondary: '#CFDDEE',
        secondaryDark: '#112031',
        tertinary: '#366271',
        tertinaryDark: '#6e9ac9',
        hoverColor: '#DEE5EE',
        hoverColorDark: '#172448',
        borderColor: '#AAC6E5',
        borderColorDark: '#2D4484',
        textColor: '#123456',
        textColorDark: '#ABCCED',
        orange: '#FFA600',
      },
      fontFamily: {
        titleFont: ['Arial', 'sans-serif'],
        textFont: ['Verdana', 'sans-serif'],
    },    
      borderRadius: {
        '4xl': '3.5rem',
      },
    },
    container: {
      center: true,
    },
  },
  variants: {
    extend: {
      scale: ['active'],
      transform: ['active'],
    },
  },
  plugins: [],
};
