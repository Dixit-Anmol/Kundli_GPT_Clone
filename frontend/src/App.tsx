import ChatPage from './pages/ChatPage'
import LoginPage from './pages/LoginPage'
import { AuthProvider, useAuth } from './context/AuthContext'

function AppContent() {
  const { user, loading } = useAuth()

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

  if (!user) {
    return <LoginPage />
  }

  return <ChatPage />
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
