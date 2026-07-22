import React, { createContext, useContext, useEffect, useState } from 'react'
import type { User } from 'firebase/auth'
import {
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  updateProfile,
  signOut,
  onAuthStateChanged,
} from 'firebase/auth'
import { auth } from '../firebase/firebase'

export interface AuthUser {
  uid: string
  email: string | null
  displayName: string | null
  photoURL: string | null
  token: string | null
}

interface AuthContextType {
  user: AuthUser | null
  firebaseUser: User | null
  loading: boolean
  token: string | null
  loginWithGoogle: () => Promise<AuthUser>
  loginWithEmail: (email: string, pass: string) => Promise<AuthUser>
  registerWithEmail: (name: string, email: string, pass: string) => Promise<AuthUser>
  logout: () => Promise<void>
  getIdToken: () => Promise<string | null>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [firebaseUser, setFirebaseUser] = useState<User | null>(null)
  const [authUser, setAuthUser] = useState<AuthUser | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  const mapUser = async (user: User | null): Promise<AuthUser | null> => {
    if (!user) return null
    const idToken = await user.getIdToken()
    setToken(idToken)
    return {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName || user.email?.split('@')[0] || 'Seeker',
      photoURL: user.photoURL,
      token: idToken,
    }
  }

  useEffect(() => {
    let unsubscribed = false
    let unsubscribe = () => {}

    // Safety timeout: Never keep the app on a loading screen for more than 2 seconds
    const timeoutId = setTimeout(() => {
      if (!unsubscribed) {
        setLoading(false)
      }
    }, 2000)

    try {
      if (auth && typeof auth === 'object') {
        unsubscribe = onAuthStateChanged(
          auth,
          async (currUser) => {
            clearTimeout(timeoutId)
            setFirebaseUser(currUser)
            if (currUser) {
              try {
                const mapped = await mapUser(currUser)
                setAuthUser(mapped)
              } catch (e) {
                console.warn('User mapping warning:', e)
              }
            } else {
              setAuthUser(null)
              setToken(null)
            }
            setLoading(false)
          },
          (err) => {
            console.error('Auth state error:', err)
            clearTimeout(timeoutId)
            setLoading(false)
          }
        )
      } else {
        clearTimeout(timeoutId)
        setLoading(false)
      }
    } catch (e) {
      console.error('onAuthStateChanged init error:', e)
      clearTimeout(timeoutId)
      setLoading(false)
    }

    return () => {
      unsubscribed = true
      clearTimeout(timeoutId)
      unsubscribe()
    }
  }, [])

  const loginWithGoogle = async (): Promise<AuthUser> => {
    const provider = new GoogleAuthProvider()
    const result = await signInWithPopup(auth, provider)
    const mapped = await mapUser(result.user)
    if (!mapped) throw new Error('Failed to extract user from Google login')
    setAuthUser(mapped)
    return mapped
  }

  const loginWithEmail = async (email: string, pass: string): Promise<AuthUser> => {
    const result = await signInWithEmailAndPassword(auth, email, pass)
    const mapped = await mapUser(result.user)
    if (!mapped) throw new Error('Failed to extract user from Email login')
    setAuthUser(mapped)
    return mapped
  }

  const registerWithEmail = async (name: string, email: string, pass: string): Promise<AuthUser> => {
    const result = await createUserWithEmailAndPassword(auth, email, pass)
    if (name && result.user) {
      await updateProfile(result.user, { displayName: name })
    }
    const mapped = await mapUser(result.user)
    if (!mapped) throw new Error('Failed to register user')
    setAuthUser(mapped)
    return mapped
  }

  const logout = async (): Promise<void> => {
    await signOut(auth)
    setAuthUser(null)
    setToken(null)
  }

  const getIdToken = async (): Promise<string | null> => {
    if (!auth.currentUser) return null
    const freshToken = await auth.currentUser.getIdToken(true)
    setToken(freshToken)
    return freshToken
  }

  return (
    <AuthContext.Provider
      value={{
        user: authUser,
        firebaseUser,
        loading,
        token,
        loginWithGoogle,
        loginWithEmail,
        registerWithEmail,
        logout,
        getIdToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
