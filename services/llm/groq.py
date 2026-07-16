import os
import requests

class GroqClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Call Groq API using HTTP requests directly (saves install size), with offline fallback."""
        if not self.api_key:
            return self._offline_fallback(user_prompt)
            
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2048
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.ok:
                res_data = response.json()
                return res_data["choices"][0]["message"]["content"]
            else:
                print(f"Groq API error response: {response.text}")
                return f"Cosmic connection failed: {response.text}\n\n{self._offline_fallback(user_prompt)}"
        except Exception as e:
            print(f"Groq network error: {e}")
            return f"Cosmic communication offline: {str(e)}\n\n{self._offline_fallback(user_prompt)}"
            
    def _offline_fallback(self, user_prompt: str) -> str:
        from services.llm.claude import AnthropicClient
        return AnthropicClient()._offline_vedic_interpretation(user_prompt)
