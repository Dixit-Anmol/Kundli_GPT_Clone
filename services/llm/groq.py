import os
import requests

class GroqClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Call Groq API using HTTP requests directly (saves install size), with offline fallback."""
        keys_to_try = [self.api_key]
        fallback_key = os.environ.get("GROQ_API_KEY_FALLBACK")
        if fallback_key and fallback_key != self.api_key:
            keys_to_try.append(fallback_key)
        fallback_key2 = os.environ.get("GROQ_API_KEY_FALLBACK2")
        if fallback_key2 and fallback_key2 not in keys_to_try:
            keys_to_try.append(fallback_key2)
            
        last_error_message = "No API key configured."
        for key in keys_to_try:
            if not key:
                continue
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {key}",
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
                    last_error_message = response.text
                    print(f"Groq API error with key {key[:12]}...: {response.text}")
            except Exception as e:
                last_error_message = str(e)
                print(f"Groq connection error with key {key[:12]}...: {e}")
                
        # If all keys fail
        return f"Cosmic connection failed: {last_error_message}\n\n{self._offline_fallback(user_prompt)}"
            
    def _offline_fallback(self, user_prompt: str) -> str:
        from services.llm.claude import AnthropicClient
        return AnthropicClient()._offline_vedic_interpretation(user_prompt)
