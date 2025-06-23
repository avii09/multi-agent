from models.database import async_db
from datetime import datetime
from collections import Counter
from pymongo import DESCENDING
from bson.regex import Regex

class MongoDBTool:
    def __init__(self):
        self.db = async_db

    # ------------------ SUPPORT AGENT METHODS ------------------

    async def search_clients(self, name=None, email=None, phone=None):
        query = {}
        if name:
            query["name"] = {"$regex": Regex(name, "i")}
        if email:
            query["email"] = {"$regex": Regex(email, "i")}
        if phone:
            query["phone"] = {"$regex": Regex(phone, "i")}
        cursor = self.db.clients.find(query)
        return await cursor.to_list(length=20)

    async def get_orders_by_client(self, client_id):
        cursor = self.db.orders.find({"client_id": client_id})
        return await cursor.to_list(length=20)

    async def get_order_by_id(self, order_id):
        return await self.db.orders.find_one({"order_id": order_id})

    async def filter_orders_by_status(self, status):
        cursor = self.db.orders.find({"status": status})
        return await cursor.to_list(length=20)

    async def get_payment_details(self, order_id):
        return await self.db.payments.find_one({"order_id": order_id})

    async def calculate_pending_dues(self, client_id):
        orders = self.db.orders.find({"client_id": client_id, "status": "pending"})
        pending_dues = 0
        async for order in orders:
            pending_dues += order.get("amount", 0)
        return {"client_id": client_id, "pending_dues": pending_dues}

    async def list_upcoming_classes(self):
        now = datetime.now()
        cursor = self.db.classes.find({"date": {"$gte": now}}).sort("date", 1)
        return await cursor.to_list(length=20)

    async def filter_classes_by_instructor(self, instructor):
        cursor = self.db.classes.find({"instructor": {"$regex": Regex(instructor, "i")}})
        return await cursor.to_list(length=20)

    # ---------------- DASHBOARD AGENT METHODS ------------------

    async def get_total_revenue(self):
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = await self.db.payments.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0

    async def get_outstanding_payments(self):
        pipeline = [
            {"$match": {"status": "pending"}},
            {"$group": {"_id": None, "outstanding": {"$sum": "$amount"}}}
        ]
        result = await self.db.orders.aggregate(pipeline).to_list(length=1)
        return result[0]["outstanding"] if result else 0

    async def count_active_inactive_clients(self):
        active = await self.db.clients.count_documents({"status": "active"})
        inactive = await self.db.clients.count_documents({"status": "inactive"})
        return {"active": active, "inactive": inactive}

    async def get_new_clients_this_month(self):
        now = datetime.now()
        first_day = datetime(now.year, now.month, 1)
        count = await self.db.clients.count_documents({"registration_date": {"$gte": first_day}})
        return {"new_clients_this_month": count}

    async def get_enrollment_trends(self):
        pipeline = [
            {"$group": {"_id": "$service_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        result = await self.db.orders.aggregate(pipeline).to_list(length=10)
        return result

    async def get_top_services(self):
        pipeline = [
            {"$group": {"_id": "$service_name", "total": {"$sum": "$amount"}}},
            {"$sort": {"total": -1}},
            {"$limit": 5}
        ]
        result = await self.db.orders.aggregate(pipeline).to_list(length=5)
        return result

    async def get_course_completion_rates(self):
        # Assume 'status' is 'active', 'completed', etc.
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        result = await self.db.courses.aggregate(pipeline).to_list(length=10)
        return result

    async def get_attendance_percentage(self, class_name):
        # Step 1: Find class_id from name
        class_doc = await self.db.classes.find_one({"name": class_name})
        if not class_doc:
            return {"error": "Class not found"}
        
        class_id = class_doc["class_id"]
        total_records = await self.db.attendance.count_documents({"class_id": class_id})
        attended = await self.db.attendance.count_documents({"class_id": class_id, "attended": True})
        
        if total_records == 0:
            return {"class": class_name, "attendance_percentage": 0}
        
        percentage = (attended / total_records) * 100
        return {"class": class_name, "attendance_percentage": round(percentage, 2)}

