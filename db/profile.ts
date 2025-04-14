import { supabase } from "../lib/supabase/browser-client"

export const getProfileByUserId = async (userId: string) => {
  const { data: profile, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("user_id", userId)
    .single()

  if (error) {
    console.error("Error getting profile:", error)
    return null
  }

  return profile
} 