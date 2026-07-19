import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import type { TabType } from './TabNavigation'
import SummaryCards from './SummaryCards'
import TabChat, { type Message } from './TabChat'

export interface TabCacheItem {
  initialReading: string
  messages: Message[]
}

interface TabPanelProps {
  tab: TabType
  chartData: any
  computed?: any
  sessionId: string
  userId?: string
  apiBaseUrl: string
  cachedData?: TabCacheItem
  onUpdateCache: (data: TabCacheItem) => void
}

export default function TabPanel({
  tab,
  chartData,
  computed,
  sessionId,
  userId,
  apiBaseUrl,
  cachedData,
  onUpdateCache,
}: TabPanelProps) {
  // Restore from parent cache if present
  const [messages, setMessages] = useState<Message[]>(cachedData?.messages || [])
  const [initialReading, setInitialReading] = useState<string>(cachedData?.initialReading || '')
  const [loadingInitial, setLoadingInitial] = useState<boolean>(!cachedData?.initialReading)
  const [loadingChat, setLoadingChat] = useState<boolean>(false)

  // Fetch initial domain reading ONLY if not already cached
  useEffect(() => {
    let cancelled = false

    async function fetchTabReading() {
      if (cachedData?.initialReading) {
        setInitialReading(cachedData.initialReading)
        setMessages(cachedData.messages || [])
        setLoadingInitial(false)
        return
      }

      setLoadingInitial(true)
      try {
        const res = await fetch(`${apiBaseUrl}/api/tab-chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: sessionId,
            user_id: userId,
            message: `Provide a detailed ${tab} analysis for my horoscope.`,
            tab: tab,
          }),
        })

        if (res.ok) {
          const data = await res.json()
          if (!cancelled) {
            setInitialReading(data.response)
            setMessages([]) // Initial reading is displayed in top card only — not duplicated in chat thread!
            onUpdateCache({ initialReading: data.response, messages: [] })
          }
        }
      } catch (err) {
        console.error(`Failed to fetch reading for tab ${tab}:`, err)
        if (!cancelled) {
          const fallback = getFallbackReading(tab, chartData)
          setInitialReading(fallback)
          setMessages([])
          onUpdateCache({ initialReading: fallback, messages: [] })
        }
      } finally {
        if (!cancelled) setLoadingInitial(false)
      }
    }

    fetchTabReading()
    return () => {
      cancelled = true
    }
  }, [tab, sessionId, userId, apiBaseUrl, cachedData?.initialReading])

  // Handle user chat message within this tab
  const handleSendMessage = async (text: string) => {
    if (!text.trim() || loadingChat) return

    const newMsgs = [...messages, { role: 'user', content: text } as Message]
    setMessages(newMsgs)
    setLoadingChat(true)

    try {
      const res = await fetch(`${apiBaseUrl}/api/tab-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          user_id: userId,
          message: text,
          tab: tab,
        }),
      })

      if (res.ok) {
        const data = await res.json()
        const updatedMsgs = [...newMsgs, { role: 'assistant', content: data.response } as Message]
        setMessages(updatedMsgs)
        onUpdateCache({ initialReading, messages: updatedMsgs })
      }
    } catch (err) {
      console.error(`Failed to send message in tab ${tab}:`, err)
      const errorMsg = {
        role: 'assistant',
        content: '🙏 I encountered a momentary connection glitch. Vedic wisdom reminds us that patience brings clarity. Please try asking again.',
      } as Message
      const updatedMsgs = [...newMsgs, errorMsg]
      setMessages(updatedMsgs)
      onUpdateCache({ initialReading, messages: updatedMsgs })
    } finally {
      setLoadingChat(false)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Summary Cards */}
      <SummaryCards tab={tab} chartData={chartData} computed={computed} />

      {/* Main Tab Initial Reading */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs">
        <div className="flex items-center justify-between border-b border-outline-variant/40 pb-4 mb-4">
          <h2 className="font-display text-2xl font-bold text-primary flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-2xl">auto_awesome</span>
            Detailed {tab.charAt(0).toUpperCase() + tab.slice(1)} Analysis
          </h2>
          <span className="text-xs text-on-surface-variant bg-surface-variant px-3 py-1 rounded-full font-medium">
            Grounded Reading
          </span>
        </div>

        {loadingInitial ? (
          <div className="py-8 flex flex-col items-center justify-center gap-3">
            <div className="w-8 h-8 border-3 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="text-xs text-on-surface-variant italic">
              Calculating {tab} planetary alignments & teachings...
            </p>
          </div>
        ) : (
          <div className="font-body text-sm leading-relaxed text-on-surface markdown-container">
            <ReactMarkdown>{initialReading}</ReactMarkdown>
          </div>
        )}
      </div>

      {/* Scoped Tab Interactive Chat */}
      <TabChat
        tab={tab}
        sessionId={sessionId}
        userId={userId}
        messages={messages}
        onSendMessage={handleSendMessage}
        loading={loadingChat}
      />
    </div>
  )
}

function getFallbackReading(tab: TabType, chartData: any): string {
  const asc = chartData?.metadata?.ascendant_sign || chartData?.ascendant_sign || 'Aries'
  const moon = chartData?.metadata?.moon_sign || chartData?.moon_sign || 'Cancer'
  return `### ✨ ${tab.charAt(0).toUpperCase() + tab.slice(1)} Overview\n\nYour **${asc} Ascendant** and **${moon} Moon** create a unique blueprint. Ask any question below to explore deep astrological insights tailored to this domain.`
}
