class ChatHistory:
    """Helper class to format and prune message lists for LLM prompts."""
    
    @staticmethod
    def format_history(history: list) -> str:
        formatted = ""
        for turn in history:
            role_label = "Astrologer" if turn["role"] == "assistant" else "Seeker"
            formatted += f"{role_label}: {turn['content']}\n"
        return formatted
