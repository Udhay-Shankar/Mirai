/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto Condensed', 'sans-serif'],
        mirai: ['"Playwrite AU TAS"', 'cursive'],
      },
      colors: {
        // Brand Colors - Clean, techy, trustworthy
        primary: '#1A73E8',       // Google-style blue for reliability
        accent: '#00E5FF',         // Futuristic neon cyan
        'dark-navy': '#0A0F1F',   // Deep premium AI-driven base
        
        // Warm Contrast - Funky/Trippy (Optimized for dark backgrounds)
        coral: '#FF6B47',          // Vibrant warm contrast - optimized luminance
        'coral-bright': '#FF8A65', // Lighter variant for extra pop
        lavender: '#E6E6FA',       // Soft calming CTA
        
        // Neutral & Supporting Colors
        'off-white': '#F5F7FA',   // Light mode backgrounds
        'text-gray': '#E0E6EE',   // Primary text on dark
        'border-gray': '#2A2F3F', // Dividers and borders
        
        // Status Colors
        success: '#00C853',        // Growth metrics
        mint: '#98FF98',           // Positive data/success states
        error: '#FF5252',          // Drops/alerts
        warning: '#FFD600',        // Cautions
        accent: {
          DEFAULT: '#059669',
          dark: '#047857',
          light: '#10B981',
        },
        warning: {
          DEFAULT: '#DC2626',
          dark: '#B91C1C',
          light: '#EF4444',
        },
        neutral: {
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'glow': '0 0 20px rgba(107, 70, 193, 0.3)',
      },
      animation: {
        'gradient-shift': 'gradientShift 20s ease infinite',
        'fade-slide-up': 'fadeSlideUp 0.6s ease-out',
        'float-in': 'floatIn 1s ease-out',
        'pulse-slow': 'pulse 8s ease-in-out infinite',
      },
      keyframes: {
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        fadeSlideUp: {
          from: {
            opacity: '0',
            transform: 'translateY(30px)',
          },
          to: {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        floatIn: {
          from: {
            opacity: '0',
            transform: 'translateY(40px) scale(0.9)',
          },
          to: {
            opacity: '1',
            transform: 'translateY(0) scale(1)',
          },
        },
        pulse: {
          '0%, 100%': {
            opacity: '0.5',
            transform: 'scale(1)',
          },
          '50%': {
            opacity: '0.8',
            transform: 'scale(1.1)',
          },
        },
      },
    },
  },
  plugins: [],
}
