import { initializeApp, getApps, getApp, type FirebaseApp } from 'firebase/app'
import { getAuth, type Auth } from 'firebase/auth'
import { getAnalytics, isSupported } from 'firebase/analytics'

// Firebase JS SDK configuration strictly loaded from environment variables
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || '',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || '',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || '',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '',
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || '',
}

let app: FirebaseApp
let auth: Auth

try {
  if (getApps().length > 0) {
    app = getApp()
  } else {
    // If real apiKey exists, use it; otherwise use safe fallback to prevent SDK throw
    const configToUse = firebaseConfig.apiKey
      ? firebaseConfig
      : {
          ...firebaseConfig,
          apiKey: 'AIzaSy_Placeholder_Configure_Render_Env_Vars',
          authDomain: 'astrosutra.firebaseapp.com',
          projectId: 'astrosutra',
          appId: '1:000000000000:web:00000000000000',
        }
    app = initializeApp(configToUse)
  }
  auth = getAuth(app)
} catch (e) {
  console.warn('[Firebase Init Handled]:', e)
  try {
    app = getApps().length > 0 ? getApp() : initializeApp({
      apiKey: 'AIzaSy_Placeholder_Configure_Render_Env_Vars',
      authDomain: 'astrosutra.firebaseapp.com',
      projectId: 'astrosutra',
      appId: '1:000000000000:web:00000000000000',
    })
    auth = getAuth(app)
  } catch (err) {
    console.error('[Firebase Fallback Error]:', err)
    app = {} as FirebaseApp
    auth = {} as Auth
  }
}

export { app, auth }

export const analyticsPromise = isSupported()
  .then((supported) => (supported && app?.name ? getAnalytics(app) : null))
  .catch(() => null)

export default app
