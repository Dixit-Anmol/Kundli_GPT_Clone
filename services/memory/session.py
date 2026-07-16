class SessionStore:
    """In-memory thread-safe session store caching birth charts, message history, keys, and usage meters."""
    
    def __init__(self):
        # Map: session_id -> { "chart_data": dict, "history": list, "key": str, "count": int }
        self.sessions = {}
        
    def create_session(self, session_id: str, api_key: str = None) -> dict:
        self.sessions[session_id] = {
            "chart_data": None,
            "history": [],
            "key": api_key,
            "count": 0
        }
        return self.sessions[session_id]
        
    def get_session(self, session_id: str) -> dict:
        if session_id not in self.sessions:
            self.create_session(session_id)
        return self.sessions[session_id]
        
    def save_chart(self, session_id: str, chart_data: dict):
        sess = self.get_session(session_id)
        sess["chart_data"] = chart_data
        
    def add_message(self, session_id: str, role: str, content: str):
        sess = self.get_session(session_id)
        sess["history"].append({"role": role, "content": content})
        sess["count"] += 1
        
    def get_history(self, session_id: str) -> list:
        sess = self.get_session(session_id)
        return sess["history"]
        
    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
            
# Global singleton instance for in-memory session persistence
session_store = SessionStore()
