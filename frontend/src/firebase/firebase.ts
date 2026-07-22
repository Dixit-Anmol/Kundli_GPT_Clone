import { initializeApp, getApps, getApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getAnalytics, isSupported } from 'firebase/analytics'
import { firebaseConfig } from '../config/firebaseConfig'

// Initialize Firebase Core App
export const app = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig)

// Export Authentication instance
export const auth = getAuth(app)

// Initialize Analytics asynchronously (safe for SSR / browser environments)
export const analyticsPromise = isSupported().then((supported) => (supported ? getAnalytics(app) : null)).catch(() => null)

export default app
