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
        'secondary-riot': "#0f1923",
      },
      fontFamily: {
        'Tungsten': ['"Tungsten"', 'sans-serif'],
        'FF-Mark' : ['"FF-Mark"', 'sans-serif']
      },
      width: {
        '1/16': '6.25%',
        '2/16': '12.50%',
        '3/16': '18.75%',
        '4/16': '25.00%',
        '5/16': '31.25%',
        '6/16': '37.50%',
        '7/16': '43.75%',
        '8/16': '50.00%',
        '9/16': '56.25%',
        '10/16': '62.50%',
        '11/16': '68.75%',
        '12/16': '75.00%',
        '13/16': '81.25%',
        '14/16': '87.50%',
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
        '1/16': '6.25%',
        '2/16': '12.50%',
        '3/16': '18.75%',
        '4/16': '25.00%',
        '5/16': '31.25%',
        '6/16': '37.50%',
        '7/16': '43.75%',
        '8/16': '50.00%',
        '9/16': '56.25%',
        '10/16': '62.50%',
        '11/16': '68.75%',
        '12/16': '75.00%',
        '13/16': '81.25%',
        '14/16': '87.50%',
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

