'use client'

import { useState } from 'react'
import { Plus, X } from 'lucide-react'
import { ScreenTimeEntry } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const CATEGORIES = [
  'Social Media',
  'Productivity',
  'Entertainment',
  'Gaming',
  'News',
  'Shopping',
  'Health & Fitness',
  'Education',
  'Other'
]

interface DataEntryFormProps {
  onSuccess: () => void
}

export default function DataEntryForm({ onSuccess }: DataEntryFormProps) {
  const [entries, setEntries] = useState<ScreenTimeEntry[]>([
    {
      date: new Date().toISOString().split('T')[0],
      app: '',
      time_minutes: 0,
      pickups: 0,
    },
  ])
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const addEntry = () => {
    setEntries([
      ...entries,
      {
        date: new Date().toISOString().split('T')[0],
        app: '',
        time_minutes: 0,
        pickups: 0,
      },
    ])
  }

  const removeEntry = (index: number) => {
    setEntries(entries.filter((_, i) => i !== index))
  }

  const updateEntry = (index: number, field: keyof ScreenTimeEntry, value: string | number) => {
    const updated = [...entries]
    updated[index] = { ...updated[index], [field]: value }
    setEntries(updated)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    setSuccess(false)

    // Validate entries
    const validEntries = entries.filter(
      (entry) => entry.app.trim() !== '' && entry.time_minutes > 0
    )

    if (validEntries.length === 0) {
      setError('Please add at least one entry with an app name and time > 0')
      setSubmitting(false)
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/entries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          entries: validEntries,
          user_id: 'default_user',
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to submit entries')
      }

      setSuccess(true)
      setEntries([
        {
          date: new Date().toISOString().split('T')[0],
          app: '',
          time_minutes: 0,
          pickups: 0,
        },
      ])
      
      // Call success callback to refresh analytics
      setTimeout(() => {
        onSuccess()
        setSuccess(false)
      }, 2000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setSubmitting(false)
    }
  }

  const inputBorder =
    'w-full px-3 py-2 border-2 border-brand-blue-dark rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-brand-pink focus:border-brand-pink'

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border-2 border-brand-blue-dark">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">
        Add Screen Time Entry
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {entries.map((entry, index) => (
          <div
            key={index}
            className="border-2 border-brand-blue-dark/60 dark:border-brand-blue-dark rounded-lg p-4 space-y-3"
          >
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Entry {index + 1}
              </span>
              {entries.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeEntry(index)}
                  className="text-red-500 hover:text-red-700"
                >
                  <X size={18} />
                </button>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Date
              </label>
              <input
                type="date"
                value={entry.date}
                onChange={(e) => updateEntry(index, 'date', e.target.value)}
                className={inputBorder}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                App Name
              </label>
              <input
                type="text"
                value={entry.app}
                onChange={(e) => updateEntry(index, 'app', e.target.value)}
                placeholder="e.g., Instagram"
                className={inputBorder}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Time (minutes)
                </label>
                <input
                  type="number"
                  value={entry.time_minutes || ''}
                  onChange={(e) => updateEntry(index, 'time_minutes', parseFloat(e.target.value) || 0)}
                  min="0"
                  step="1"
                  className={inputBorder}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Pickups
                </label>
                <input
                  type="number"
                  value={entry.pickups || ''}
                  onChange={(e) => updateEntry(index, 'pickups', parseInt(e.target.value) || 0)}
                  min="0"
                  step="1"
                  className={inputBorder}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                Category (optional - auto-detected if not provided)
              </label>
              <select
                value={entry.category || ''}
                onChange={(e) => updateEntry(index, 'category', e.target.value || '')}
                className={inputBorder}
              >
                <option value="">Auto-detect</option>
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          </div>
        ))}

        <button
          type="button"
          onClick={addEntry}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 border-2 border-dashed border-brand-blue-dark rounded-lg text-slate-600 dark:text-slate-400 hover:border-brand-pink hover:text-brand-pink transition-colors"
        >
          <Plus size={20} />
          Add Another Entry
        </button>

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-lg p-3">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        {success && (
          <div className="bg-green-50 dark:bg-green-900/20 border-2 border-green-200 dark:border-green-800 rounded-lg p-3">
            <p className="text-sm text-green-600 dark:text-green-400">
              ✅ Entries submitted successfully! Refreshing analytics...
            </p>
          </div>
        )}

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-brand-blue-dark hover:opacity-90 disabled:bg-slate-400 text-white font-semibold py-3 px-4 rounded-lg transition-opacity"
        >
          {submitting ? 'Submitting...' : 'Submit Entries'}
        </button>
      </form>
    </div>
  )
}
