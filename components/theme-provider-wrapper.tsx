"use client"

import { ThemeProvider } from "./theme-provider"

export function ThemeProviderWrapper({ 
  children 
}: { 
  children: React.ReactNode 
}) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
} 