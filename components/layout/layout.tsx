import * as React from "react"

interface LayoutProps {
  children: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b bg-white p-4">
        <h1 className="text-xl font-bold">Chatbot UI</h1>
      </header>

      <main className="flex-1 bg-gray-50">{children}</main>

      <footer className="border-t bg-white p-4 text-center text-sm text-gray-600">
        © 2024 Chatbot UI. All rights reserved.
      </footer>
    </div>
  )
} 