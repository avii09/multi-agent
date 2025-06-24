from fastapi import APIRouter, Body
from fastapi.responses import Response
from typing import Optional
from bson import json_util
from tools.mongodb_tool import MongoDBTool
from tools.external_api_tool import ExternalAPITool

router = APIRouter()
tool = MongoDBTool()
external_tool = ExternalAPITool()

def json_mongo(data):
    return Response(content=json_util.dumps(data), media_type="application/json")

# ------------------ Support Agent Test Routes ------------------

@router.get("/test/search_clients")
async def search_clients(name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None):
    result = tool.search_clients(name=name, email=email, phone=phone)
    return json_mongo(result)

@router.get("/test/orders_by_client")
async def orders_by_client(client_id: str):
    result = tool.get_orders_by_client(client_id)
    return json_mongo(result)

@router.get("/test/order_by_id")
async def order_by_id(order_id: str):
    result = tool.get_order_by_id(order_id)
    return json_mongo(result)

@router.get("/test/orders_by_status")
async def orders_by_status(status: str):
    result = tool.filter_orders_by_status(status)
    return json_mongo(result)

@router.get("/test/payment_details")
async def payment_details(order_id: str):
    result = tool.get_payment_details(order_id)
    return json_mongo(result)

@router.get("/test/pending_dues")
async def pending_dues(client_id: str):
    result = tool.calculate_pending_dues(client_id)
    return json_mongo(result)

@router.get("/test/upcoming_classes")
async def upcoming_classes():
    result = tool.list_upcoming_classes()
    return json_mongo(result)

@router.get("/test/classes_by_instructor")
async def classes_by_instructor(instructor: str):
    result = tool.filter_classes_by_instructor(instructor)
    return json_mongo(result)

# ------------------ Dashboard Agent Test Routes ------------------

@router.get("/test/total_revenue")
async def total_revenue():
    result = tool.get_total_revenue()
    return json_mongo(result)

@router.get("/test/outstanding_payments")
async def outstanding_payments():
    result = tool.get_outstanding_payments()
    return json_mongo(result)

@router.get("/test/client_counts")
async def client_counts():
    result = tool.count_active_inactive_clients()
    return json_mongo(result)

@router.get("/test/new_clients_this_month")
async def new_clients_this_month():
    result = tool.get_new_clients_this_month()
    return json_mongo(result)

@router.get("/test/enrollment_trends")
async def enrollment_trends():
    result = tool.get_enrollment_trends()
    return json_mongo(result)

@router.get("/test/top_services")
async def top_services():
    result = tool.get_top_services()
    return json_mongo(result)

@router.get("/test/completion_rates")
async def completion_rates():
    result = tool.get_course_completion_rates()
    return json_mongo(result)

@router.get("/test/attendance_percentage")
async def attendance_percentage(class_name: str):
    result = tool.get_attendance_percentage(class_name)
    return json_mongo(result)

# ------------------ External API Test Routes ------------------

@router.post("/test/create_client_enquiry")
async def create_client_enquiry(client_data: dict = Body(...)):
    result = external_tool.create_client_enquiry(client_data)
    return json_mongo(result)

