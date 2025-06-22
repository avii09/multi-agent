from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


#order status
class OrderStatus(str, Enum):
    PAID = "paid"
    PENDING = "pending"
    CANCELLED = "cancelled"

#client status
class ClientStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

#class status
class ClassStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


#client collection
class Client(BaseModel):
    client_id: str = Field(..., description="Unique client identifier")
    name: str
    email: str
    phone: str
    enrolled_services: List[str] = []  # List of course/class IDs
    status: ClientStatus = ClientStatus.ACTIVE
    registration_date: datetime
    birthday: Optional[datetime] = None
    address: Optional[str] = None


#order collection
class Order(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    client_id: str
    service_id: str  # course or class ID
    service_type: str  # "course" or "class"
    service_name: str
    amount: float
    status: OrderStatus = OrderStatus.PENDING
    order_date: datetime
    due_date: Optional[datetime] = None


#payment collection
class Payment(BaseModel):
    payment_id: str = Field(..., description="Unique payment identifier")
    order_id: str
    client_id: str
    amount: float
    payment_date: datetime
    payment_method: str  # "card", "cash", "upi"
    transaction_id: Optional[str] = None


#course collection
class Course(BaseModel):
    course_id: str = Field(..., description="Unique course identifier")
    name: str
    description: str
    instructor: str
    duration_weeks: int
    price: float
    max_students: int
    enrolled_count: int = 0
    start_date: datetime
    end_date: datetime
    status: str = "active"


#class collection
class Class(BaseModel):
    class_id: str = Field(..., description="Unique class identifier")
    name: str
    instructor: str
    date: datetime
    duration_minutes: int
    max_students: int
    enrolled_students: List[str] = []  # List of client IDs
    status: ClassStatus = ClassStatus.SCHEDULED
    price: float


#attendance collection
class Attendance(BaseModel):
    attendance_id: str = Field(..., description="Unique attendance identifier")
    class_id: str
    client_id: str
    date: datetime
    attended: bool
    notes: Optional[str] = None 
