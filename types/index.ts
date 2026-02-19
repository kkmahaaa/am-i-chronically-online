export interface ScreenTimeEntry {
  date: string
  app: string
  time_minutes: number
  category?: string
  pickups?: number
}

export interface EntriesRequest {
  entries: ScreenTimeEntry[]
  user_id?: string
}

export interface Metrics {
  total_screen_time_hours: number
  total_screen_time_minutes: number
  doomscroll_hours: number
  total_pickups: number
  avg_pickups_per_day: number
  days_tracked: number
  category_breakdown: Record<string, number>
  daily_totals: Array<{
    date: string
    time_hours: number
    pickups: number
  }>
  weekly_totals: Array<{
    period: string
    time_hours: number
    pickups: number
  }>
  top_apps: Record<string, number>
}

export interface ChronicScore {
  score: number
  level: string
  description: string
  breakdown: {
    time_score: number
    doomscroll_score: number
    pickup_score: number
    avg_hours_per_day: number
    doomscroll_percentage: number
  }
}

export interface Tip {
  title: string
  description: string
  priority: 'high' | 'medium' | 'low'
  category: string
}

export interface AnalyticsData {
  success: boolean
  metrics: Metrics
  chronic_score: ChronicScore
  tips: Tip[]
  processed_entries_count: number
  total_entries?: number
}
