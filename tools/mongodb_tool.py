from models.database import sync_db
from datetime import datetime
from collections import Counter
from pymongo import DESCENDING
from bson.regex import Regex

class MongoDBTool:
    def __init__(self):
        self.db = sync_db

    # ------------------ SUPPORT AGENT METHODS ------------------

    def search_clients(self, name=None, email=None, phone=None):
        query = {}
        if name:
            query["name"] = {"$regex": Regex(name, "i")}
        if email:
            query["email"] = {"$regex": Regex(email, "i")}
        if phone:
            query["phone"] = {"$regex": Regex(phone, "i")}
        return list(self.db.clients.find(query).limit(20))

    def get_orders_by_client(self, client_id):
        return list(self.db.orders.find({"client_id": client_id}).limit(20))

    def get_order_by_id(self, order_id):
        return self.db.orders.find_one({"order_id": order_id})

    def filter_orders_by_status(self, status):
        return list(self.db.orders.find({"status": status}).limit(20))

    def get_payment_details(self, order_id):
        return self.db.payments.find_one({"order_id": order_id})

    def calculate_pending_dues(self, client_id):
        orders = self.db.orders.find({"client_id": client_id, "status": "pending"})
        pending_dues = sum(order.get("amount", 0) for order in orders)
        return {"client_id": client_id, "pending_dues": pending_dues}

    def list_upcoming_classes(self):
        now = datetime.now()
        return list(self.db.classes.find({"date": {"$gte": now}}).sort("date", 1).limit(20))

    def filter_classes_by_instructor(self, instructor):
        return list(self.db.classes.find({
            "instructor": {"$regex": Regex(instructor, "i")}
        }).limit(20))

    # ---------------- DASHBOARD AGENT METHODS ------------------

    def get_total_revenue(self):
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.db.payments.aggregate(pipeline))
        return result[0]["total"] if result else 0

    def get_outstanding_payments(self):
        pipeline = [
            {"$match": {"status": "pending"}},
            {"$group": {"_id": None, "outstanding": {"$sum": "$amount"}}}
        ]
        result = list(self.db.orders.aggregate(pipeline))
        return result[0]["outstanding"] if result else 0

    def count_active_inactive_clients(self):
        active = self.db.clients.count_documents({"status": "active"})
        inactive = self.db.clients.count_documents({"status": "inactive"})
        return {"active": active, "inactive": inactive}

    def get_new_clients_this_month(self):
        now = datetime.now()
        first_day = datetime(now.year, now.month, 1)
        count = self.db.clients.count_documents({"registration_date": {"$gte": first_day}})
        return {"new_clients_this_month": count}

    def get_enrollment_trends(self):
        pipeline = [
            {"$group": {"_id": "$service_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.db.orders.aggregate(pipeline))

    def get_top_services(self):
        pipeline = [
            {"$group": {"_id": "$service_name", "total": {"$sum": "$amount"}}},
            {"$sort": {"total": -1}},
            {"$limit": 5}
        ]
        return list(self.db.orders.aggregate(pipeline))

    def get_course_completion_rates(self):
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        return list(self.db.courses.aggregate(pipeline))

    def get_attendance_percentage(self, class_name):
        class_doc = self.db.classes.find_one({"name": class_name})
        if not class_doc:
            return {"error": "Class not found"}
        
        class_id = class_doc["class_id"]
        total_records = self.db.attendance.count_documents({"class_id": class_id})
        attended = self.db.attendance.count_documents({"class_id": class_id, "attended": True})
        
        if total_records == 0:
            return {"class": class_name, "attendance_percentage": 0}
        
        percentage = (attended / total_records) * 100
        return {"class": class_name, "attendance_percentage": round(percentage, 2)}

