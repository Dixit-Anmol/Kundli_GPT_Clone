import { useState } from 'react'
import ChatPage from './pages/ChatPage'
import LoginPage from './pages/LoginPage'
import LandingPage from './pages/LandingPage'
import PricingPage from './pages/PricingPage'
import { AuthProvider, useAuth } from './context/AuthContext'

type AppView = 'landing' | 'login' | 'pricing' | 'app'

function AppContent() {
  const { user, loading } = useAuth()
  const [view, setView] = useState<AppView>('landing')

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FAF8F3] flex flex-col items-center justify-center space-y-4 font-sans">
        <div className="w-12 h-12 border-4 border-amber-500 border-t-transparent rounded-full animate-spin shadow-md" />
        <p className="text-sm font-semibold text-on-surface-variant animate-pulse">
          Connecting to AstroSutra AI...
        </p>
      </div>
    )
  }

  // If user is already authenticated, go straight to the app
  if (user) {
    return <ChatPage />
  }

  // Show login page
  if (view === 'login') {
    return (
      <LoginPage
        onClose={() => setView('landing')}
        onSuccess={() => {
          // After successful login, ChatPage will render because user becomes non-null
        }}
      />
    )
  }

  // Show pricing page
  if (view === 'pricing') {
    return <PricingPage onNavigateBack={() => setView('landing')} />
  }

  // Default: show the landing page
  return (
    <LandingPage
      onSignIn={() => setView('login')}
      onGetStarted={() => setView('login')}
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
