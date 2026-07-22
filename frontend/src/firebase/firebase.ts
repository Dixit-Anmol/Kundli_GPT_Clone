import { initializeApp, getApps, getApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getAnalytics, isSupported } from 'firebase/analytics'

// Firebase JS SDK configuration strictly read from environment variables (VITE_FIREBASE_*)
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
}

// Initialize Firebase Core App strictly from environment configuration
export const app = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig)

// Export Authentication instance
export const auth = getAuth(app)

// Initialize Analytics asynchronously (safe for browser environments)
export const analyticsPromise = isSupported().then((supported) => (supported ? getAnalytics(app) : null)).catch(() => null)

export default app
