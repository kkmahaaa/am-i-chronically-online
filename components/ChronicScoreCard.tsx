'use client'

import { ChronicScore } from '@/types'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface ChronicScoreCardProps {
  score: ChronicScore
}

export default function ChronicScoreCard({ score }: ChronicScoreCardProps) {
  const getScoreColor = (score: number) => {
    if (score < 20) return 'text-green-600 dark:text-green-400'
    if (score < 40) return 'text-blue-600 dark:text-blue-400'
    if (score < 60) return 'text-yellow-600 dark:text-yellow-400'
    if (score < 80) return 'text-orange-600 dark:text-orange-400'
    return 'text-red-600 dark:text-red-400'
  }

  // Level badge: solid background so white text is readable
  const getScoreBgColor = (score: number) => {
    if (score < 20) return 'bg-green-500 dark:bg-green-600'
    if (score < 40) return 'bg-blue-500 dark:bg-blue-600'
    if (score < 60) return 'bg-yellow-500 dark:bg-yellow-600'
    if (score < 80) return 'bg-orange-500 dark:bg-orange-600'
    return 'bg-red-500 dark:bg-red-600'
  }

  const getScoreBorderColor = (score: number) => {
    if (score < 20) return 'border-green-500'
    if (score < 40) return 'border-blue-500'
    if (score < 60) return 'border-yellow-500'
    if (score < 80) return 'border-orange-500'
    return 'border-red-500'
  }

  const getTrendIcon = (score: number) => {
    const iconColor = getScoreColor(score)
    if (score < 20) return <TrendingDown className={iconColor} size={24} />
    if (score < 60) return <Minus className={iconColor} size={24} />
    return <TrendingUp className={iconColor} size={24} />
  }

  const hasBreakdown =
    score.breakdown &&
    typeof score.breakdown.time_score === 'number' &&
    typeof score.breakdown.avg_hours_per_day === 'number'

  return (
    <div
      className={`bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border-2 ${getScoreBorderColor(
        score.score
      )}`}
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
          Your Chronic Online Score
        </h2>
        {getTrendIcon(score.score)}
      </div>

      <div className="flex items-center gap-6">
        <div className={`text-6xl font-bold ${getScoreColor(score.score)}`}>
          {score.score}
          <span className={`text-2xl ${getScoreColor(score.score)}`}>/100</span>
        </div>

        <div className="flex-1">
          <div
            className={`inline-block px-4 py-2 rounded-full font-semibold mb-2 text-white ${getScoreBgColor(
              score.score
            )}`}
          >
            {score.level}
          </div>
          <p className="text-slate-600 dark:text-slate-300">{score.description}</p>
        </div>
      </div>

      <div className={`mt-6 pt-6 border-t-2 ${getScoreBorderColor(score.score)} border-opacity-50`}>
        <h3 className={`text-sm font-semibold mb-3 ${getScoreColor(score.score)}`}>
          Score Breakdown:
        </h3>
        {hasBreakdown ? (
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-slate-600 dark:text-slate-400">Screen Time</p>
              <p className="font-semibold text-slate-900 dark:text-white">
                {score.breakdown!.time_score}/40 pts
              </p>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {score.breakdown!.avg_hours_per_day.toFixed(1)} hrs/day
              </p>
            </div>
            <div>
              <p className="text-slate-600 dark:text-slate-400">Social Media</p>
              <p className="font-semibold text-slate-900 dark:text-white">
                {score.breakdown!.doomscroll_score}/30 pts
              </p>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {score.breakdown!.doomscroll_percentage.toFixed(0)}% of total
              </p>
            </div>
            <div>
              <p className="text-slate-600 dark:text-slate-400">Pickups</p>
              <p className="font-semibold text-slate-900 dark:text-white">
                {score.breakdown!.pickup_score}/30 pts
              </p>
            </div>
          </div>
        ) : (
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Submit entries to see your score breakdown.
          </p>
        )}
      </div>
    </div>
  )
}
