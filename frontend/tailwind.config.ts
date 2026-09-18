import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './index.html',
    './src/**/*.{ts,tsx,js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Eduvia brand colors
        brand: {
          50:  '#f0f4ff',
          100: '#e0eaff',
          200: '#c7d7fe',
          300: '#a5bbfc',
          400: '#8198f8',
          500: '#6272f1',
          600: '#4f52e5',
          700: '#4240ca',
          800: '#3638a3',
          900: '#303581',
          950: '#1d1f4b',
        },
        // Accessible warm accent
        accent: {
          50:  '#fff8f0',
          100: '#feefd8',
          200: '#fddcaf',
          300: '#fcc27d',
          400: '#fa9e49',
          500: '#f87f22',
          600: '#e96312',
          700: '#c24a11',
          800: '#9b3b15',
          900: '#7d3215',
          950: '#441707',
        },
        // Semantic colors
        success: {
          DEFAULT: '#22c55e',
          foreground: '#ffffff',
        },
        warning: {
          DEFAULT: '#f59e0b',
          foreground: '#ffffff',
        },
        destructive: {
          DEFAULT: '#ef4444',
          foreground: '#ffffff',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        // Accessibility: minimum 16px body text
        'learner-sm':  ['1rem',    { lineHeight: '1.6' }],
        'learner-md':  ['1.25rem', { lineHeight: '1.7' }],
        'learner-lg':  ['1.5rem',  { lineHeight: '1.8' }],
        'learner-xl':  ['2rem',    { lineHeight: '1.5' }],
      },
      spacing: {
        // Accessibility: minimum 44×44px touch targets
        'touch-min': '2.75rem',
        'touch-comfortable': '3rem',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      animation: {
        'fade-in':    'fadeIn 0.3s ease-out',
        'slide-up':   'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-in':  'bounceIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%':   { opacity: '0', transform: 'translateY(-8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%':      { opacity: '0.7' },
        },
        bounceIn: {
          '0%':   { opacity: '0', transform: 'scale(0.8)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('tailwindcss-animate'),
  ],
}

export default config
