'use client'

import { Metrics } from '@/types'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

interface ChartsSectionProps {
  metrics: Metrics
}

const COLORS = [
  '#5870D6', // brand blue
  '#E04899', // brand pink
  '#DB48E0', // brand purple
  '#4659b8', // blue-dark
  '#10b981', // green
  '#f59e0b', // yellow
  '#ef4444', // red
  '#f97316', // orange
]

export default function ChartsSection({ metrics }: ChartsSectionProps) {
  const categoryBreakdown = metrics?.category_breakdown ?? {}
  const topApps = metrics?.top_apps ?? {}
  const dailyTotals = metrics?.daily_totals ?? []

  // Prepare category data for pie chart
  const categoryData = Object.entries(categoryBreakdown).map(([name, value]) => ({
    name,
    value: Number(Number(value).toFixed(1)),
  }))

  // Prepare top apps data for bar chart
  const topAppsData = Object.entries(topApps)
    .slice(0, 10)
    .map(([name, value]) => ({
      name: name.length > 15 ? name.substring(0, 15) + '...' : name,
      hours: Number(Number(value).toFixed(1)),
    }))
    .reverse()

  // Prepare daily totals for line chart
  const dailyData = dailyTotals.map((day) => ({
    date: new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    hours: Number((day.time_hours ?? 0).toFixed(1)),
    pickups: day.pickups ?? 0,
  }))

  return (
    <div className="space-y-6">
      {/* Daily Trends Line Chart */}
      {dailyData.length > 0 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border-2 border-brand-blue-dark">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Daily Screen Time Trends
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dailyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#4659b8" strokeOpacity={0.4} />
              <XAxis dataKey="date" stroke="#4659b8" />
              <YAxis stroke="#4659b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '2px solid #4659b8',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="hours"
                stroke="#DB48E0"
                strokeWidth={2}
                name="Hours"
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Category Breakdown Pie Chart */}
      {categoryData.length > 0 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border-2 border-brand-blue-dark">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4">
            Category Breakdown
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '2px solid #4659b8',
                  borderRadius: '8px',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Top Apps Bar Chart */}
      {topAppsData.length > 0 && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border-2 border-brand-blue-dark">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Top Apps</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topAppsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#4659b8" strokeOpacity={0.4} />
              <XAxis dataKey="name" stroke="#4659b8" tick={{ fontSize: 12 }} />
              <YAxis stroke="#4659b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '2px solid #4659b8',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="hours" fill="#E04899" name="Hours" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
