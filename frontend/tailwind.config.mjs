/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        "boardroom": "#101a2e",
        "charcoal": "#232f44",
        "riskred": "#c2372c",
        "riskamber": "#d97706",
        "riskblue": "#2563eb"
},
      fontFamily: {
        "display": [
                "'Source Serif 4'",
                "Georgia",
                "serif"
        ],
        "body": [
                "'Inter'",
                "system-ui",
                "sans-serif"
        ],
        "mono": [
                "'JetBrains Mono'",
                "ui-monospace",
                "monospace"
        ],
        "serif": [
                "'Source Serif 4'",
                "Georgia",
                "serif"
        ],
        "sans": [
                "'Inter'",
                "system-ui",
                "sans-serif"
        ]
},
    },
  },
  plugins: [],
};
