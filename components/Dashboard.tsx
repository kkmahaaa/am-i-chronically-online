'use client'

import { AnalyticsData } from '@/types'
import ChronicScoreCard from './ChronicScoreCard'
import MetricsCards from './MetricsCards'
import ChartsSection from './ChartsSection'
import TipsSection from './TipsSection'

interface DashboardProps {
  data: AnalyticsData
  /** When true, only render charts and tips (score/metrics rendered by page) */
  chartsAndTipsOnly?: boolean
}

export default function Dashboard({ data, chartsAndTipsOnly = false }: DashboardProps) {
  if (chartsAndTipsOnly) {
    return (
      <div className="space-y-6">
        <ChartsSection metrics={data.metrics} />
        <TipsSection tips={data.tips} />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <ChronicScoreCard score={data.chronic_score} />
      <MetricsCards metrics={data.metrics} />
      <ChartsSection metrics={data.metrics} />
      <TipsSection tips={data.tips} />
    </div>
  )
}
