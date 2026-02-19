'use client'

import { useState, useEffect } from 'react'
import DataEntryForm from '@/components/DataEntryForm'
import ChronicScoreCard from '@/components/ChronicScoreCard'
import MetricsCards from '@/components/MetricsCards'
import ChartsSection from '@/components/ChartsSection'
import TipsSection from '@/components/TipsSection'
import { AnalyticsData } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_BASE_URL}/api/analytics`)
      if (!response.ok) {
        throw new Error('Failed to fetch analytics')
      }
      const data = await response.json()
      setAnalytics(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      console.error('Error fetching analytics:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const handleEntrySubmit = async () => {
    await fetchAnalytics()
  }

  const emptyOrErrorBlock = loading ? (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8 text-center border-2 border-brand-blue-dark">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-purple mx-auto"></div>
      <p className="mt-4 text-slate-600 dark:text-slate-300">Loading analytics...</p>
    </div>
  ) : error ? (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8 border-2 border-brand-blue-dark">
      <div className="text-red-600 dark:text-red-400">
        <p className="font-semibold">Error loading analytics</p>
        <p className="text-sm mt-2">{error}</p>
        <button
          onClick={fetchAnalytics}
          className="mt-4 px-4 py-2 bg-brand-blue-dark text-white rounded-lg hover:opacity-90"
        >
          Retry
        </button>
      </div>
    </div>
  ) : (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8 text-center border-2 border-brand-blue-dark">
      <p className="text-slate-600 dark:text-slate-300">
        No data yet. Submit your first entry to see analytics!
      </p>
    </div>
  )

  return (
    <main className="min-h-screen bg-[#4659b8] dark:bg-[#1e3a5f]">
      <div className="mx-auto px-4 sm:px-6 py-6 md:py-8 max-w-4xl">
        <header className="text-center mb-6 md:mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-800 dark:text-white mb-2">
            Am I Chronically Online?
          </h1>
          <p className="text-slate-700 dark:text-slate-200 text-base md:text-lg">
            Monitor your screen time and uncover your digital habits
          </p>
        </header>

        {/* 1. Add Screen Time Entry - top */}
        <section className="mb-6">
          <DataEntryForm onSuccess={handleEntrySubmit} />
        </section>

        {/* 2. Chronic Score - thin wide block */}
        {analytics && (
          <section className="mb-6">
            <ChronicScoreCard score={analytics.chronic_score} />
          </section>
        )}

        {/* 3. Four metric cards */}
        {analytics && (
          <section className="mb-6">
            <MetricsCards metrics={analytics.metrics} />
          </section>
        )}

        {/* 4–6. Three content blocks: charts + tips (or placeholder) */}
        {analytics ? (
          <section className="space-y-6">
            <ChartsSection metrics={analytics.metrics} />
            <TipsSection tips={analytics.tips} />
          </section>
        ) : (
          <section className="mt-6">
            {emptyOrErrorBlock}
          </section>
        )}
      </div>
    </main>
  )
}
