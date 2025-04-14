export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      assistant_collections: {
        Row: {
          assistant_id: string
          collection_id: string
          created_at: string
          updated_at: string | null
          user_id: string
        }
        Insert: {
          assistant_id: string
          collection_id: string
          created_at?: string
          updated_at?: string | null
          user_id: string
        }
        Update: {
          assistant_id?: string
          collection_id?: string
          created_at?: string
          updated_at?: string | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "assistant_collections_assistant_id_fkey"
            columns: ["assistant_id"]
            isOneToOne: false
            referencedRelation: "assistants"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "assistant_collections_collection_id_fkey"
            columns: ["collection_id"]
            isOneToOne: false
            referencedRelation: "collections"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "assistant_collections_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      workspaces: {
        Row: {
          id: string
          user_id: string
          name: string
          description: string | null
          instructions: string | null
          created_at: string
          updated_at: string | null
          image_path: string | null
          sharing: string | null
          is_home: boolean
        }
        Insert: {
          id?: string
          user_id: string
          name: string
          description?: string | null
          instructions?: string | null
          created_at?: string
          updated_at?: string | null
          image_path?: string | null
          sharing?: string | null
          is_home?: boolean
        }
        Update: {
          id?: string
          user_id?: string
          name?: string
          description?: string | null
          instructions?: string | null
          created_at?: string
          updated_at?: string | null
          image_path?: string | null
          sharing?: string | null
          is_home?: boolean
        }
        Relationships: [
          {
            foreignKeyName: "workspaces_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      profiles: {
        Row: {
          id: string
          user_id: string
          has_onboarded: boolean
          display_name: string | null
        }
        Insert: {
          id?: string
          user_id: string
          has_onboarded?: boolean
          display_name?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          has_onboarded?: boolean
          display_name?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "profiles_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: true
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      assistants: {
        Row: {
          id: string
          user_id: string
          name: string
        }
        Insert: {
          id?: string
          user_id: string
          name: string
        }
        Update: {
          id?: string
          user_id?: string
          name?: string
        }
        Relationships: [
          {
            foreignKeyName: "assistants_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      collections: { Row: { id: string } }
      chats: { Row: { id: string } }
      files: { Row: { id: string } }
      folders: { Row: { id: string } }
      models: { Row: { id: string } }
      presets: { Row: { id: string } }
      prompts: { Row: { id: string } }
      tools: { Row: { id: string } }
      file_items: { Row: { id: string } }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
  }
}

export type Tables<T extends keyof Database['public']['Tables']> = Database['public']['Tables'][T]['Row'] 