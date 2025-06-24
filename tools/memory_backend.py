# tools/memory_backend.py
from pymongo import MongoClient
from datetime import datetime
import os

class MongoMemoryBackend:
    def __init__(self):
        mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.client = MongoClient(mongo_url)
        self.db = self.client["crew_memory"]
        self.collection = self.db["memory_sessions"]

    def save_memory(self, session_id: str, message: str):
        """Store user message in memory under session ID."""
        self.collection.insert_one({
            "session_id": session_id,
            "message": message,
            "timestamp": datetime.utcnow()
        })

    def get_memory(self, session_id: str, limit=5):
        """Fetch recent messages for session ID."""
        docs = self.collection.find(
            {"session_id": session_id}
        ).sort("timestamp", -1).limit(limit)
        return [doc["message"] for doc in reversed(list(docs))]
