'use client'

import { Tip } from '@/types'
import { AlertCircle, Info, Lightbulb } from 'lucide-react'

interface TipsSectionProps {
  tips: Tip[]
}

export default function TipsSection({ tips }: TipsSectionProps) {
  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high':
        return <AlertCircle className="text-red-500" size={20} />
      case 'medium':
        return <Info className="text-brand-pink" size={20} />
      default:
        return <Lightbulb className="text-brand-purple" size={20} />
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'border-l-red-500 bg-red-50 dark:bg-red-900/10'
      case 'medium':
        return 'border-l-brand-pink bg-pink-50 dark:bg-pink-900/10'
      default:
        return 'border-l-brand-purple bg-purple-50 dark:bg-purple-900/10'
    }
  }

  if (tips.length === 0) {
    return null
  }

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border-2 border-brand-blue-dark">
      <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">
        Personalized Tips
      </h3>
      <div className="space-y-4">
        {tips.map((tip, index) => (
          <div
            key={index}
            className={`border-l-4 rounded-r-lg p-4 ${getPriorityColor(tip.priority)}`}
          >
            <div className="flex items-start gap-3">
              <div className="mt-0.5">{getPriorityIcon(tip.priority)}</div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="font-semibold text-slate-900 dark:text-white">{tip.title}</h4>
                  <span className="text-xs px-2 py-1 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 uppercase">
                    {tip.priority}
                  </span>
                </div>
                <p className="text-slate-700 dark:text-slate-300 text-sm leading-relaxed">
                  {tip.description}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
