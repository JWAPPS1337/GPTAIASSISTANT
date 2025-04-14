"use server"

// Define any necessary types locally
export const getWorkspacesByUserId = async (userId: string) => {
  // Mock implementation
  return [
    {
      id: "default-workspace",
      name: "Default Workspace",
      user_id: userId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
  ]
} 