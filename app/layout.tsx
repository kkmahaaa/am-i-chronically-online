import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Am I Chronically Online?',
  description: 'Analyze your screen time habits and get personalized tips',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
