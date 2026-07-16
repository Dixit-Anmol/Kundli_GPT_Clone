import os
from services.llm.claude import AnthropicClient
from services.llm.groq import GroqClient

class LLMFactory:
    @staticmethod
    def get_client(provider: str = None):
        """Factory method to resolve the active LLM provider (defaulting to environment variables)."""
        if not provider:
            provider = os.environ.get("LLM_PROVIDER", "groq")
            
        provider = provider.lower()
        
        if provider in ["claude", "anthropic", "anthropic_claude"]:
            return AnthropicClient()
        elif provider == "groq":
            return GroqClient()
        else:
            return GroqClient()
            
def generate_response(system_prompt: str, user_prompt: str, provider: str = None) -> str:
    client = LLMFactory.get_client(provider)
    return client.generate(system_prompt, user_prompt)
