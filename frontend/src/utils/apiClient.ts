import { auth } from '../firebase/firebase'

export async function getAuthHeader(): Promise<Record<string, string>> {
  const currentUser = auth.currentUser
  if (currentUser) {
    try {
      const token = await currentUser.getIdToken()
      return { Authorization: `Bearer ${token}` }
    } catch (e) {
      console.warn('Failed to get Firebase ID token:', e)
    }
  }
  return {}
}

export async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const authHeader = await getAuthHeader()
  const headers = {
    'Content-Type': 'application/json',
    ...authHeader,
    ...(options.headers || {}),
  }

  return fetch(url, {
    ...options,
    headers,
  })
}
