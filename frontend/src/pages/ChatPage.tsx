import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import Navbar from '../components/layout/Navbar'
import ChatInputBar from '../components/chat/ChatInputBar'
import AssistantMessage from '../components/chat/AssistantMessage'
import BirthDetailsForm from '../components/chat/BirthDetailsForm'
import BirthplaceMap from '../components/chat/BirthplaceMap'
import ComputingCard from '../components/chat/ComputingCard'
import HoroscopeSummary from '../components/chat/HoroscopeSummary'
import SuggestionChips from '../components/chat/SuggestionChips'
import type { BirthData } from '../components/chat/BirthDetailsForm'

type ChatStep = 'welcome' | 'birthplace' | 'computing' | 'ready'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'
  : 'https://kundli-gpt-clone-back.onrender.com'

export default function ChatPage() {
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [inputValue, setInputValue] = useState('')
  const [step, setStep] = useState<ChatStep>('welcome')
  const [birthData, setBirthData] = useState<BirthData | null>(null)
  
  // Real computed horoscope data from backend
  const [chartData, setChartData] = useState<any>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [loadingChat, setLoadingChat] = useState(false)

  const handleBirthSubmit = (data: BirthData) => {
    setBirthData(data)
    setStep('birthplace')
  }

  const handleBirthplaceConfirm = async (_placeName: string, lat: number, lon: number) => {
    if (!birthData) return
    setStep('computing')

    try {
      // 1. Fetch real chart data from FastAPI backend
      const response = await fetch(`${API_BASE_URL}/api/chart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: birthData.fullName,
          date_str: birthData.dateOfBirth,
          time_str: `${birthData.timeOfBirth}:00`,
          latitude: lat,
          longitude: lon,
          session_id: sessionId,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setChartData(data)
        setStep('ready')

        // 2. Fetch the initial birth chart interpretation response
        setLoadingChat(true)
        const chatRes = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            session_id: sessionId,
            message: "Analyze my birth chart and explain my placements.",
          }),
        })

        if (chatRes.ok) {
          const chatDataJson = await chatRes.json()
          setMessages([
            { role: 'assistant', content: chatDataJson.response }
          ])
        }
      }
    } catch (err) {
      console.error('Failed to calculate horoscope chart:', err)
      // Fallback for offline/development environments
      setTimeout(() => {
        setChartData({
          ascendant_sign: 'Libra',
          moon_sign: 'Cancer',
          nakshatra: 'Pushya',
          pada: 2,
          yogas: [{ name: 'Gaja Kesari Yoga', meaning: 'Jupiter in Kendra from Moon' }],
          doshas: {
            manglik: { is_present: true, description: 'Mars in 7th house' },
            kaal_sarp: { is_present: false },
            sade_sati: { is_present: false }
          }
        })
        setMessages([
          { 
            role: 'assistant', 
            content: '🙏 Blessings. I have calculated your Vedic Birth Chart. Your Ascendant is Libra, Moon Sign is Cancer, and you are currently in a Jupiter Mahadasha. How may I guide you on your Dharma today?' 
          }
        ])
        setStep('ready')
      }, 2000)
    } finally {
      setLoadingChat(false)
    }
  }

  const handleSend = async (messageText?: string) => {
    const textToSend = messageText || inputValue
    if (!textToSend.trim() || loadingChat) return

    // Append user message immediately
    const updatedMessages = [...messages, { role: 'user', content: textToSend } as Message]
    setMessages(updatedMessages)
    setInputValue('')
    setLoadingChat(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: textToSend,
        }),
      })

      if (response.ok) {
        const chatDataJson = await response.json()
        setMessages(prev => [
          ...prev,
          { role: 'assistant', content: chatDataJson.response }
        ])
      }
    } catch (err) {
      console.error('Failed to send message:', err)
      // Mock fallback answer
      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          { 
            role: 'assistant', 
            content: `Blessings. In response to your question: "${textToSend}", Vedic wisdom teaches us to focus on our action (Karma) without attachment to the results. Your Cancer Moon sign makes you highly sensitive; ground yourself in meditation.` 
          }
        ])
      }, 1000)
    } finally {
      setLoadingChat(false)
    }
  }

  const handleSuggestion = (text: string) => {
    handleSend(text)
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Main Chat Content */}
      <main className="relative z-10 max-w-[800px] mx-auto px-4 pt-12 pb-[180px]">
        <div className="space-y-6">
          {/* Welcome Message */}
          <AssistantMessage icon="star">
            🙏 Namaste! Welcome. I'll prepare your personalized horoscope and become your spiritual
            assistant. Before we begin, I need a few birth details.
          </AssistantMessage>

          {/* Birth Details Form */}
          {step === 'welcome' && <BirthDetailsForm onSubmit={handleBirthSubmit} />}

          {/* Birthplace Selection */}
          {(step === 'birthplace' || step === 'computing') && (
            <>
              <AssistantMessage icon="location_on">
                Great{birthData ? `, ${birthData.fullName}` : ''}! Now I need your birthplace.
                Please search your city or drop a pin on the map.
              </AssistantMessage>
              {step === 'birthplace' && <BirthplaceMap onConfirm={handleBirthplaceConfirm} />}
            </>
          )}

          {/* Computing State */}
          {step === 'computing' && (
            <ComputingCard steps={[
              { label: 'Finding Planetary Positions', status: 'active', progress: 45 },
              { label: 'Calculating Houses', status: 'waiting' },
              { label: 'Computing Nakshatras', status: 'waiting' },
            ]} />
          )}

          {/* Horoscope Ready & Interactive Q&A */}
          {step === 'ready' && chartData && (
            <>
              {/* Ready Summary Card */}
              <HoroscopeSummary
                details={[
                  { label: 'Ascendant (Lagna)', value: chartData.ascendant_sign },
                  { label: 'Moon Sign (Rashi)', value: chartData.moon_sign },
                  { label: 'Current Dasha', value: 'Jupiter' },  // Can be calculated dynamically
                  { label: 'Nakshatra', value: chartData.nakshatra },
                ]}
                todaysEnergy={
                  chartData.doshas?.manglik?.is_present 
                    ? '"Mars is active in your relationship quadrant. Focus on patience and non-violent communication. A good day for introspective studies."'
                    : '"A harmonious day for ventures. Sun in your 10th house indicates focus and professional alignment. Stay committed to your path."'
                }
                onViewComplete={() => console.log('View complete horoscope')}
              />

              {/* Chat Thread */}
              <div className="space-y-6 mt-10 border-t border-outline-variant/30 pt-10">
                {messages.map((msg, i) => (
                  msg.role === 'assistant' ? (
                    <AssistantMessage key={i} icon="auto_awesome">
                      <div className="font-body leading-relaxed text-on-surface markdown-container">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    </AssistantMessage>
                  ) : (
                    <div key={i} className="flex justify-end animate-fade-in-up">
                      <div className="max-w-[85%] bg-primary-fixed border border-primary/20 text-on-primary-fixed rounded-2xl rounded-tr-none p-4 text-[16px] leading-6 shadow-sm font-medium">
                        {msg.content}
                      </div>
                    </div>
                  )
                ))}
                
                {/* Typing Loader */}
                {loadingChat && (
                  <div className="flex gap-4 items-center pl-4 py-2 opacity-70">
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200" />
                  </div>
                )}
              </div>

              {/* Suggestion Chips */}
              {!loadingChat && (
                <SuggestionChips
                  suggestions={[
                    'Explain my birth chart',
                    'Career Guidance',
                    'Marriage Compatibility',
                    'Gemstone Recommendation',
                    'Health Forecast',
                  ]}
                  onSelect={handleSuggestion}
                />
              )}
            </>
          )}
        </div>
      </main>

      {/* Floating Chat Input */}
      {step === 'ready' && (
        <ChatInputBar 
          value={inputValue} 
          onChange={setInputValue} 
          onSend={() => handleSend()} 
        />
      )}
    </div>
  )
}
