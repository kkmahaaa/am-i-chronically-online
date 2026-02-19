'use client'

import { Metrics } from '@/types'
import { Clock, Smartphone, TrendingUp, Calendar } from 'lucide-react'

interface MetricsCardsProps {
  metrics: Metrics
}

export default function MetricsCards({ metrics }: MetricsCardsProps) {
  const hours = metrics?.total_screen_time_hours ?? 0
  const minutes = metrics?.total_screen_time_minutes ?? 0
  const doomscroll = metrics?.doomscroll_hours ?? 0
  const avgPickups = metrics?.avg_pickups_per_day ?? 0
  const totalPickups = metrics?.total_pickups ?? 0
  const daysTracked = metrics?.days_tracked ?? 0

  const cards = [
    {
      title: 'Total Screen Time',
      value: `${hours.toFixed(1)} hrs`,
      subtitle: `${minutes} minutes`,
      icon: Clock,
      color: 'bg-brand-blue',
    },
    {
      title: 'Doomscroll Hours',
      value: `${doomscroll.toFixed(1)} hrs`,
      subtitle: 'Social media time',
      icon: Smartphone,
      color: 'bg-brand-pink',
    },
    {
      title: 'Avg Pickups/Day',
      value: `${avgPickups.toFixed(0)}`,
      subtitle: `${totalPickups} total pickups`,
      icon: TrendingUp,
      color: 'bg-brand-purple',
    },
    {
      title: 'Days Tracked',
      value: `${daysTracked}`,
      subtitle: 'Days of data',
      icon: Calendar,
      color: 'bg-brand-blue-dark',
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card, index) => {
        const Icon = card.icon
        return (
          <div
            key={index}
            className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-4 border-2 border-brand-blue-dark"
          >
            <div className="flex items-center justify-between mb-2">
              <div className={`${card.color} p-2 rounded-lg`}>
                <Icon className="text-white" size={20} />
              </div>
            </div>
            <h3 className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-1">
              {card.title}
            </h3>
            <p className="text-2xl font-bold text-slate-900 dark:text-white">{card.value}</p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{card.subtitle}</p>
          </div>
        )
      })}
    </div>
  )
}
