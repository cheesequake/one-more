/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-riot': "#ff4654",
      },
      fontFamily: {
        'Tungsten': ['"Tungsten"', 'sans-serif'],
        'FF-Mark' : ['"FF-Mark"', 'sans-serif']
      },
      width: {
        '15/16': '93.75%',
      },
      height: {
        '10vh': '10vh',
        '20vh': '20vh',
        '30vh': '30vh',
        '40vh': '40vh',
        '50vh': '50vh',
        '60vh': '60vh',
        '70vh': '70vh',
        '80vh': '80vh',
        '90vh': '90vh',
        '15/16': '93.75%',
      },
      minHeight: {
        '10vh': '10vh',
        '20vh': '20vh',
        '30vh': '30vh',
        '40vh': '40vh',
        '50vh': '50vh',
        '60vh': '60vh',
        '70vh': '70vh',
        '80vh': '80vh',
        '90vh': '90vh',
        '5/6': '83.33333333%',
        '11/12': '91.6666666667%',
        '15/16': '93.75%',
      },
      maxHeight: {
        '5/6': '83.33333333%',
        '11/12': '91.6666666667%',
      },
    },
  },
  plugins: [],
}

