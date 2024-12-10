/* @type {import('tailwindcss').Config} */
export default  {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"], // Inclut tous les fichiers pertinents
  theme: {
    extend: {
      spacing: {
        128: "32rem", // 512px
        144: "36rem", // 576px
      },
    },
  },
  plugins: [],
};
