/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "blue-main": "#285D85",
      },
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
};

//MY CONFIG

// module.exports = {
//   content: ["./src/**/*.{js,jsx,ts,tsx}"],
//   theme: {
//     extend: {
//       colors: {
//         "blue-main": "#285D85",
//       },
//       fontFamily: {
//         roboto: ["Roboto", "sans-serif"],
//       },
//     },
//   },
//   plugins: [],
// };
