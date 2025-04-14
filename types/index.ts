export interface ChatMessage {
  role: "system" | "user" | "assistant" | "function" | "tool"
  content: string
  id?: string
  // Add more properties as needed
}

export interface ChatSettings {
  model: string
  prompt: string
  temperature: number
  contextLength: number
  includeProfileContext: boolean
  includeWorkspaceInstructions: boolean
  embeddingsProvider: string
}

export type ModelProvider = 
  | "openai" 
  | "google" 
  | "anthropic" 
  | "mistral" 
  | "groq" 
  | "perplexity" 
  | "ollama" 
  | "custom" 
  | "openrouter"

export interface LLM {
  modelId: string
  modelName: string
  provider: ModelProvider
  hostedId?: string
  // Add more properties as needed
}

export interface OpenRouterLLM extends LLM {
  // Add OpenRouter specific properties
  contextWindow?: number
}

export interface WorkspaceImage {
  workspaceId: string
  path: string
  base64: string
  url: string
}

export interface MessageImage {
  messageId: string
  path: string
  base64: string
  url: string
}

export interface ChatFile {
  id: string
  name: string
  type: string
  // Add more properties as needed
}

export interface VALID_ENV_KEYS {
  // Add environment key types
} 