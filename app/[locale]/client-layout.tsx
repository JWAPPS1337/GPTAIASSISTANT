"use client"

import { GlobalState } from "../../components/utility/global-state"
import { Providers } from "../../components/utility/providers"
import TranslationsProvider from "../../components/utility/translations-provider"
import { Toaster } from "../../components/ui/sonner"
import { ReactNode } from "react"

interface ClientLayoutProps {
  children: ReactNode
  session: any
  locale: string
  resources: any
  namespaces: string[]
}

export default function ClientLayout({ 
  children, 
  session, 
  locale, 
  resources, 
  namespaces 
}: ClientLayoutProps) {
  return (
    <Providers attribute="class" defaultTheme="dark">
      <TranslationsProvider
        namespaces={namespaces}
        locale={locale}
        resources={resources}
      >
        <Toaster richColors position="top-center" duration={3000} />
        <div className="bg-background text-foreground flex h-dvh flex-col items-center overflow-x-auto">
          {session ? <GlobalState>{children}</GlobalState> : children}
        </div>
      </TranslationsProvider>
    </Providers>
  )
} 