import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        brand: {
          blue: '#5870D6',
          pink: '#E04899',
          purple: '#DB48E0',
          'blue-dark': '#4659b8', // darker shade for borders
        },
      },
    },
  },
  plugins: [],
}
export default config
