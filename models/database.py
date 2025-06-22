from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fitness_studio")

# data seeding synchronous operations
sync_client = MongoClient(MONGODB_URL)
sync_db = sync_client[DATABASE_NAME]

# fastapi async operations
async_client = AsyncIOMotorClient(MONGODB_URL)
async_db = async_client[DATABASE_NAME]


COLLECTIONS = {
    "clients": "clients",
    "orders": "orders", 
    "payments": "payments",
    "courses": "courses",
    "classes": "classes",
    "attendance": "attendance"
}

def get_sync_collection(collection_name: str):
    """Get synchronous collection for data operations"""
    return sync_db[COLLECTIONS[collection_name]]

async def get_async_collection(collection_name: str):
    """Get asynchronous collection for API operations"""
    return async_db[COLLECTIONS[collection_name]]

def test_connection():
    """Test MongoDB connection"""
    try:
        sync_client.admin.command('ping')
        print("MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False
