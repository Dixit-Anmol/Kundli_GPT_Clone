import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getAnalytics, isSupported } from 'firebase/analytics'

// Firebase JS SDK configuration read from environment variables with fallback defaults
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyBngPVS1uH69_QbIUVZr_Dpu7jNcngUe7U",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "astrosutraai-b524e.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "astrosutraai-b524e",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "astrosutraai-b524e.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "29791277131",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:29791277131:web:641a2e6b6216b959d43dce",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "G-59WZT4JJQY",
}

// Initialize Firebase Core App safely
export const app = initializeApp(firebaseConfig)

// Initialize Firebase Authentication and export auth instance
export const auth = getAuth(app)

// Initialize Analytics asynchronously (safe for SSR / browser compatibility)
export const analyticsPromise = isSupported().then((supported) => (supported ? getAnalytics(app) : null)).catch(() => null)

export default app
