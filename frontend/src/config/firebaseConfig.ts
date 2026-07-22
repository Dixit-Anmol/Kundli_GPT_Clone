/**
 * Firebase Client SDK Configuration.
 * Reads from VITE_FIREBASE_* environment variables with public client fallbacks
 * to ensure seamless production builds on Render & static hosts.
 */
export const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyBngPVS1uH69_QbIUVZr_Dpu7jNcngUe7U",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "astrosutraai-b524e.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "astrosutraai-b524e",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "astrosutraai-b524e.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "29791277131",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:29791277131:web:641a2e6b6216b959d43dce",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "G-59WZT4JJQY",
}
