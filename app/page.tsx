"use client"

import { GlobalState } from "@/components/utility/global-state"

export default function Home() {
  return (
    <GlobalState>
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <h1 className="text-4xl font-bold mb-4">Welcome to Local AI Assistant</h1>
        <p className="text-xl">Your personal AI assistant that runs locally</p>
      </main>
    </GlobalState>
  )
} 