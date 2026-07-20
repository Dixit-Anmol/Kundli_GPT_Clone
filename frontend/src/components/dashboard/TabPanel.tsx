import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import type { TabType } from './TabNavigation'
import SummaryCards from './SummaryCards'
import TabChat, { type Message } from './TabChat'
import AnimatedKundliChart from './AnimatedKundliChart'
import PlanetaryTable from './PlanetaryTable'
import RelationshipTargetSelector, { type RelationshipTarget } from './RelationshipTargetSelector'
import RelationshipScoreCard from './RelationshipScoreCard'
import CareerSubTabNavigation, { type CareerSubTab } from './CareerSubTabNavigation'
import KalaVidyaDashboard from './KalaVidyaDashboard'
import PrashnaDashboardView from './PrashnaDashboardView'

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
  tabCacheMap?: Record<string, TabCacheItem>
  onUpdateCacheByKey?: (key: string, data: TabCacheItem) => void
}

export default function TabPanel({
  tab,
  chartData,
  computed,
  sessionId,
  userId,
  apiBaseUrl,
  tabCacheMap = {},
  onUpdateCacheByKey,
}: TabPanelProps) {
  const [relationshipTarget, setRelationshipTarget] = useState<RelationshipTarget>('spouse')
  const [careerSubTab, setCareerSubTab] = useState<CareerSubTab>('overview')

  // Compute unique key for granular caching
  const getCacheKey = () => {
    if (tab === 'marriage') return `marriage_${relationshipTarget}`
    if (tab === 'career') return `career_${careerSubTab}`
    return tab
  }

  const cacheKey = getCacheKey()
  const cachedItem = tabCacheMap[cacheKey]

  const [messages, setMessages] = useState<Message[]>(cachedItem?.messages || [])
  const [initialReading, setInitialReading] = useState<string>(cachedItem?.initialReading || '')
  const [loadingInitial, setLoadingInitial] = useState<boolean>(!cachedItem?.initialReading)
  const [loadingChat, setLoadingChat] = useState<boolean>(false)

  // Sync state if cached item exists or cache key changes
  useEffect(() => {
    let cancelled = false
    const currentKey = getCacheKey()
    const existing = tabCacheMap[currentKey]

    if (existing?.initialReading) {
      setInitialReading(existing.initialReading)
      setMessages(existing.messages || [])
      setLoadingInitial(false)
      return
    }

    async function fetchTabReading() {
      setLoadingInitial(true)
      try {
        let queryMsg = `Provide a detailed ${tab} analysis for my horoscope.`
        if (tab === 'marriage') {
          queryMsg = `Provide a detailed ${relationshipTarget} relationship analysis for my horoscope.`
        } else if (tab === 'career' && (careerSubTab === 'kala_vidya' || (careerSubTab as string) === 'receptivity')) {
          queryMsg = `Provide a detailed Kala, Vidya (64 classical talents), Student Receptivity (Shishya Grahana), and research pedagogy analysis for my horoscope.`
        }



        const res = await fetch(`${apiBaseUrl}/api/tab-chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: sessionId,
            user_id: userId,
            message: queryMsg,
            tab: tab,
            is_initial: true,
            relationship_type: relationshipTarget,
            sub_tab: careerSubTab,
          }),
        })

        if (res.ok) {
          const data = await res.json()
          if (!cancelled) {
            setInitialReading(data.response)
            setMessages([])
            if (onUpdateCacheByKey) {
              onUpdateCacheByKey(currentKey, { initialReading: data.response, messages: [] })
            }
          }
        }
      } catch (err) {
        console.error(`Failed to fetch reading for tab ${tab}:`, err)
        if (!cancelled) {
          const fallback = getFallbackReading(tab, chartData)
          setInitialReading(fallback)
          setMessages([])
          if (onUpdateCacheByKey) {
            onUpdateCacheByKey(currentKey, { initialReading: fallback, messages: [] })
          }
        }
      } finally {
        if (!cancelled) setLoadingInitial(false)
      }
    }

    fetchTabReading()
    return () => {
      cancelled = true
    }
  }, [tab, relationshipTarget, careerSubTab, sessionId, userId, apiBaseUrl])

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
          is_initial: false,
          relationship_type: relationshipTarget,
          sub_tab: careerSubTab,
        }),
      })


      if (res.ok) {
        const data = await res.json()
        const updatedMsgs = [...newMsgs, { role: 'assistant', content: data.response } as Message]
        setMessages(updatedMsgs)
        if (onUpdateCacheByKey) {
          onUpdateCacheByKey(getCacheKey(), { initialReading, messages: updatedMsgs })
        }
      }
    } catch (err) {
      console.error(`Failed to send message in tab ${tab}:`, err)
      const errorMsg = {
        role: 'assistant',
        content: '🙏 I encountered a momentary connection glitch. Vedic wisdom reminds us that patience brings clarity. Please try asking again.',
      } as Message
      const updatedMsgs = [...newMsgs, errorMsg]
      setMessages(updatedMsgs)
      if (onUpdateCacheByKey) {
        onUpdateCacheByKey(getCacheKey(), { initialReading, messages: updatedMsgs })
      }
    } finally {

      setLoadingChat(false)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Sub-Tab Navigation for Career Module */}
      {tab === 'career' && (
        <CareerSubTabNavigation
          activeSubTab={careerSubTab}
          onSubTabChange={setCareerSubTab}
        />
      )}

      {/* Summary Cards */}
      <SummaryCards tab={tab} chartData={chartData} computed={computed} />

      {/* Interactive Animated Kundli Chart OR Prashna / Partial View (Overview Tab Only) */}
      {tab === 'overview' && (
        <>
          {chartData?.mode === 'prashna' || chartData?.mode === 'partial' ? (
            <PrashnaDashboardView chartData={chartData} />
          ) : (
            <>
              <AnimatedKundliChart chartData={chartData} />
              <PlanetaryTable chartData={chartData} />
            </>
          )}
        </>
      )}


      {/* Interactive Multi-Target Relationship Engine (Marriage Tab Only) */}
      {tab === 'marriage' && (
        <>
          <RelationshipTargetSelector
            selectedTarget={relationshipTarget}
            onSelectTarget={setRelationshipTarget}
          />
          <RelationshipScoreCard
            target={relationshipTarget}
            chartData={chartData}
          />
        </>
      )}

      {/* Kala, Vidya & Student Receptivity Interactive Dashboard (Career Sub-Tab Only) */}
      {tab === 'career' && careerSubTab === 'kala_vidya' && (
        <KalaVidyaDashboard chartData={chartData} />
      )}



      {/* Main Tab Personal AI Reading Card */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs">
        <div className="flex items-center justify-between border-b border-outline-variant/40 pb-4 mb-4">
          <h2 className="font-display text-2xl font-bold text-primary flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-2xl">auto_awesome</span>
            {tab === 'marriage'
              ? `${relationshipTarget.charAt(0).toUpperCase() + relationshipTarget.slice(1)} Relationship AI Analysis`
              : tab === 'career' && careerSubTab === 'kala_vidya'
              ? 'Personal AI Astrological Analysis (Kala, Vidya & Receptivity)'
              : `Detailed ${tab.charAt(0).toUpperCase() + tab.slice(1)} Analysis`}
          </h2>
          <span className="text-xs text-on-surface-variant bg-surface-variant px-3 py-1 rounded-full font-medium">
            Personal AI Reading
          </span>
        </div>

        {loadingInitial ? (
          <div className="py-8 flex flex-col items-center justify-center gap-3">
            <div className="w-8 h-8 border-3 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="text-xs text-on-surface-variant italic">
              Generating personal AI astrological analysis for your chart...
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
