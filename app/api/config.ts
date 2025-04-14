export const API_BASE_URL = 'http://localhost:5001';

export const API_ENDPOINTS = {
  QUERY: '/query',
  DOCUMENTS: '/documents',
  UPLOAD: '/upload'
};

export const makeRequest = async (endpoint: string, method: 'GET' | 'POST' = 'GET', body?: any) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}; 