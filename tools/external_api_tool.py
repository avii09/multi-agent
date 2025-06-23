from models.database import async_db
from datetime import datetime
import uuid

class ExternalAPITool:
    def __init__(self):
        self.db = async_db

    async def create_client_enquiry(self, client_data: dict):
        """
        simulate creation of a new client enquiry in the 'clients' collection.
        required: name, email, phone
        optional: birthday, address
        """
        client = {
            "client_id": f"CLIENT_{uuid.uuid4().hex[:8].upper()}",
            "name": client_data["name"],
            "email": client_data["email"],
            "phone": client_data["phone"],
            "enrolled_services": client_data.get("enrolled_services", []),
            "status": "active",
            "registration_date": datetime.utcnow(),
            "birthday": client_data.get("birthday"),
            "address": client_data.get("address")
        }

        await self.db.clients.insert_one(client)
        return {"message": "Client enquiry created", "client_id": client["client_id"]}


    async def create_order(self, client_id: str, service_info: dict):
        """
        Simulate order creation using client_id + service (course/class) info.
        service_info = {
            "service_id": "COURSE_001",
            "service_type": "course",
            "service_name": "Yoga Beginner",
            "amount": 2500
        }
        """
        order_id = f"ORDER_{uuid.uuid4().hex[:8].upper()}"
        order = {
            "order_id": order_id,
            "client_id": client_id,
            "service_id": service_info["service_id"],
            "service_type": service_info["service_type"],
            "service_name": service_info["service_name"],
            "amount": service_info["amount"],
            "status": "pending",
            "order_date": datetime.utcnow(),
            "due_date": datetime.utcnow()
        }
        await self.db.orders.insert_one(order)
        return {"message": "Order created", "order_id": order_id}

