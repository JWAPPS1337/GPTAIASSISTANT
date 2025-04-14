"use client"

import * as React from "react"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Textarea } from "../ui/textarea"
import { Card } from "../ui/card"
import { Avatar } from "../ui/avatar"
import { Loader2, Send, FileText, User, Bot, Database } from "lucide-react"
import { ScrollArea } from "../ui/scroll-area"
import { config } from "@/lib/config"
import { localAuth } from "@/lib/auth/browser-client"
import { Switch } from "../ui/switch"
import { Label } from "../ui/label"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  createdAt?: string
  sources?: {
    file_name: string
    score?: number
    text: string
  }[]
}

export const ChatUI: React.FC = () => {
  const [messages, setMessages] = React.useState<Message[]>([])
  const [input, setInput] = React.useState("")
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [useRAG, setUseRAG] = React.useState(false)
  const messagesEndRef = React.useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  React.useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      createdAt: new Date().toISOString()
    }
    
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsLoading(true)
    setError(null)

    try {
      // Format messages for the chat API
      const apiMessages = [...messages, userMessage].map(msg => ({
        role: msg.role,
        content: msg.content
      }))
      
      // Get the authentication token
      const token = localAuth.auth.getToken()
      
      // Prepare the headers with authentication if available
      const headers: Record<string, string> = {
        "Content-Type": "application/json"
      }
      
      if (token) {
        headers["Authorization"] = `Bearer ${token}`
      }
      
      // Call the chat API
      const response = await fetch(`${config.api.url}/chat`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          messages: apiMessages,
          temperature: 0.7,
          use_rag: useRAG  // Include the RAG flag
        })
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }

      const data = await response.json()
      
      // Add the assistant's response
      const assistantMessage: Message = {
        id: data.id || Date.now().toString(),
        role: "assistant",
        content: data.content,
        createdAt: new Date().toISOString(),
        sources: data.sources
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      console.error("Error sending message:", err)
      setError(err instanceof Error ? err.message : "An unknown error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col bg-background">
      <div className="flex items-center justify-between border-b px-4 py-3">
        <h1 className="text-xl font-bold">Local AI Assistant</h1>
        <div className="flex items-center space-x-2">
          <Switch 
            id="rag-mode" 
            checked={useRAG} 
            onCheckedChange={setUseRAG}
            disabled={isLoading}
          />
          <Label htmlFor="rag-mode" className="flex items-center cursor-pointer">
            <Database className="mr-1 h-4 w-4" />
            <span className="text-sm">Document Knowledge</span>
          </Label>
        </div>
      </div>
      
      <ScrollArea className="flex-1 p-4">
        <div className="mx-auto max-w-3xl space-y-4 pb-20">
          {messages.length === 0 ? (
            <div className="flex h-[60vh] flex-col items-center justify-center text-center text-muted-foreground">
              <Bot size={64} className="mb-4 opacity-50" />
              <h3 className="mb-2 text-lg font-medium">Welcome to Local AI Assistant</h3>
              <p className="max-w-sm text-sm">
                Powered by Ollama running Mistral AI locally. Your data stays on your device.
              </p>
              {useRAG && (
                <p className="mt-2 max-w-sm text-sm font-medium text-primary">
                  Document Knowledge mode is ON. Assistant will use your documents to answer questions.
                </p>
              )}
            </div>
          ) : (
            messages.map(message => (
              <div key={message.id} className="flex flex-col gap-2">
                <div className="flex items-start gap-3">
                  <Avatar>
                    {message.role === "user" ? (
                      <User className="h-6 w-6" />
                    ) : (
                      <Bot className="h-6 w-6" />
                    )}
                  </Avatar>
                  <Card className={`max-w-[85%] p-4 ${message.role === "assistant" ? "bg-muted" : ""}`}>
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-3 border-t pt-2">
                        <p className="mb-1 text-xs font-medium text-muted-foreground">Sources:</p>
                        <div className="space-y-1">
                          {message.sources.map((source, i) => (
                            <div key={i} className="flex items-start gap-1 text-xs">
                              <FileText className="mt-0.5 h-3 w-3 shrink-0 text-muted-foreground" />
                              <span className="font-medium">{source.file_name}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </Card>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
          
          {error && (
            <Card className="border-red-300 bg-red-50 p-3 text-sm text-red-800">
              Error: {error}
            </Card>
          )}
          
          {isLoading && (
            <div className="flex items-center justify-center py-4">
              <Loader2 className="h-6 w-6 animate-spin text-primary" />
            </div>
          )}
        </div>
      </ScrollArea>
      
      <div className="border-t bg-background p-4">
        <form onSubmit={handleSubmit} className="mx-auto max-w-3xl">
          <div className="flex items-end gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={`Type your message${useRAG ? ' (Document Knowledge mode ON)' : ''}...`}
              className="min-h-[60px] flex-1 resize-none"
              disabled={isLoading}
              onKeyDown={e => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  handleSubmit(e)
                }
              }}
            />
            <Button type="submit" size="icon" disabled={isLoading || !input.trim()}>
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </Button>
          </div>
          <p className="mt-2 text-center text-xs text-muted-foreground">
            All interactions are processed locally. Your data never leaves your device.
          </p>
        </form>
      </div>
    </div>
  )
}
