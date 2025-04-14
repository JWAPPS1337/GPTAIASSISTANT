"use client"

import { ChatbotUISVG } from "../../components/icons/chatbotui-svg"
import { IconArrowRight } from "@tabler/icons-react"
import { useTheme } from "next-themes"
import Link from "next/link"

export default function HomePage() {
  const { theme } = useTheme()

  return (
    <div className="flex size-full flex-col items-center justify-center">
      <div>
        <ChatbotUISVG theme={theme === "dark" ? "dark" : "light"} scale={0.3} />
      </div>

      <div className="mt-2 text-4xl font-bold">Local AI Assistant</div>
      
      <div className="mt-4 text-center text-gray-600 dark:text-gray-400 max-w-md">
        Your personal AI assistant that runs completely on your machine. 
        Train it for your specific needs while keeping your data private.
      </div>

      <Link
        className="mt-6 flex w-[200px] items-center justify-center rounded-md bg-blue-500 p-2 font-semibold text-white hover:bg-blue-600 transition-colors"
        href="/chat"
      >
        Start Assistant
        <IconArrowRight className="ml-1" size={20} />
      </Link>
    </div>
  )
}
