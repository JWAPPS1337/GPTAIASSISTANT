export const getProfileByUserId = async (userId: string) => {
  // Mock implementation
  return {
    id: userId,
    user_id: userId,
    has_onboarded: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
} 