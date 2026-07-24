import { useState, useEffect } from 'react'
import ChatPage from './pages/ChatPage'
import LoginPage from './pages/LoginPage'
import LandingPage from './pages/LandingPage'
import PricingPage from './pages/PricingPage'
import { AuthProvider, useAuth } from './context/AuthContext'

type AppView = 'landing' | 'login' | 'pricing' | 'app'

function AppContent() {
  const { user, loading } = useAuth()
  
  // Scoped to the individual browser tab
  const [view, setView] = useState<AppView>(() => {
    const saved = sessionStorage.getItem('last_view') as AppView | null
    return saved === 'app' ? 'app' : 'landing'
  })

  const [hasClickedSign, setHasClickedSign] = useState(() => {
    const saved = sessionStorage.getItem('last_view')
    return saved === 'app'
  })

  // Keep track of the active view in sessionStorage
  useEffect(() => {
    sessionStorage.setItem('last_view', view)
  }, [view])

  // Listen to state changes after user requests authentication
  useEffect(() => {
    if (hasClickedSign && !loading) {
      if (user) {
        setView('app')
      } else {
        setView('landing')
        setHasClickedSign(false)
      }
    }
  }, [hasClickedSign, loading, user])

  // Handle logout transition
  useEffect(() => {
    if (!user && view === 'app') {
      setView('landing')
      setHasClickedSign(false)
    }
  }, [user, view])

  // Show pricing page
  if (view === 'pricing') {
    return <PricingPage onNavigateBack={() => setView('landing')} />
  }

  // Show loading spinner only when verification is active and state is loading
  if (hasClickedSign && loading) {
    return (
      <div className="min-h-screen bg-[#FAF8F3] flex flex-col items-center justify-center space-y-4 font-sans">
        <div className="w-12 h-12 border-4 border-amber-500 border-t-transparent rounded-full animate-spin shadow-md" />
        <p className="text-sm font-semibold text-on-surface-variant animate-pulse">
          Connecting to AstroSutra AI...
        </p>
      </div>
    )
  }

  // Route to the app (ChatPage) when authenticated and active
  if (view === 'app' && user) {
    return <ChatPage />
  }

  // Show login page
  if (view === 'login') {
    return (
      <LoginPage
        onClose={() => {
          setView('landing')
          setHasClickedSign(false)
        }}
        onSuccess={() => {
          setView('app')
        }}
      />
    )
  }

  // Default: show the landing page (no blocking spinner on initial mount)
  return (
    <LandingPage
      onSignIn={() => setHasClickedSign(true)}
      onGetStarted={() => setHasClickedSign(true)}
      onPricing={() => setView('pricing')}
    />
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
