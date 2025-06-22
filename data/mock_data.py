from faker import Faker
import random
from datetime import datetime, timedelta
from models.schemas import *
import uuid

fake = Faker()

def generate_clients(count=100):
    """Generate realistic client data"""
    clients = []
    for i in range(count):
        client = {
            "client_id": f"CLIENT_{i+1:04d}",
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number()[:15],
            "enrolled_services": [],
            "status": random.choice(["active", "inactive"]),
            "registration_date": fake.date_time_between(start_date='-2y', end_date='now'),
            'birthday': fake.date_time_between(start_date='-80y', end_date='-18y'),
            "address": fake.address()
        }
        clients.append(client)
    return clients

def generate_courses(count=10):
    """Generate course data"""
    course_names = [
        "Yoga Beginner", "Yoga Advanced", "Pilates Fundamentals", 
        "HIIT Training", "Strength Training", "Cardio Blast",
        "Meditation & Mindfulness", "Dance Fitness", "CrossFit", "Zumba"
    ]
    
    instructors = [
        "Sarah Johnson", "Mike Chen", "Priya Sharma", "David Wilson",
        "Lisa Rodriguez", "James Kumar", "Emily Davis", "Alex Thompson"
    ]
    
    courses = []
    for i, name in enumerate(course_names):
        course = {
            "course_id": f"COURSE_{i+1:03d}",
            "name": name,
            "description": f"Professional {name.lower()} training program",
            "instructor": random.choice(instructors),
            "duration_weeks": random.randint(4, 12),
            "price": random.randint(2000, 8000),
            "max_students": random.randint(10, 25),
            "enrolled_count": random.randint(5, 20),
            "start_date": fake.date_time_between(start_date='-1y', end_date='+3m'),
            "end_date": fake.date_time_between(start_date='+3m', end_date='+1y'),
            "status": "active"
        }
        courses.append(course)
    return courses

def generate_classes(count=50):
    """Generate class data"""
    class_names = [
        "Morning Yoga", "Evening Pilates", "HIIT Workout", "Strength Session",
        "Cardio Burn", "Meditation Class", "Dance Party", "CrossFit WOD"
    ]
    
    instructors = [
        "Sarah Johnson", "Mike Chen", "Priya Sharma", "David Wilson",
        "Lisa Rodriguez", "James Kumar", "Emily Davis", "Alex Thompson"
    ]
    
    classes = []
    for i in range(count):
        class_date = fake.date_time_between(start_date='-1m', end_date='+1m')
        class_obj = {
            "class_id": f"CLASS_{i+1:04d}",
            "name": random.choice(class_names),
            "instructor": random.choice(instructors),
            "date": class_date,
            "duration_minutes": random.choice([45, 60, 90]),
            "max_students": random.randint(8, 20),
            "enrolled_students": [f"CLIENT_{random.randint(1, 100):04d}" for _ in range(random.randint(3, 15))],
            "status": random.choice(["scheduled", "ongoing", "completed"]),
            "price": random.randint(500, 1500)
        }
        classes.append(class_obj)
    return classes

def generate_orders(clients, courses, classes, count=200):
    """Generate order data"""
    orders = []
    all_services = []
    
    # Add courses as services
    for course in courses:
        all_services.append({
            "id": course["course_id"],
            "name": course["name"],
            "type": "course",
            "price": course["price"]
        })
    
    # Add classes as services  
    for class_obj in classes:
        all_services.append({
            "id": class_obj["class_id"],
            "name": class_obj["name"],
            "type": "class",
            "price": class_obj["price"]
        })
    
    for i in range(count):
        client = random.choice(clients)
        service = random.choice(all_services)
        order_date = fake.date_time_between(start_date='-6m', end_date='now')
        
        order = {
            "order_id": f"ORDER_{i+1:05d}",
            "client_id": client["client_id"],
            "service_id": service["id"],
            "service_type": service["type"],
            "service_name": service["name"],
            "amount": service["price"],
            "status": random.choice(["paid", "pending", "cancelled"]),
            "order_date": order_date,
            "due_date": order_date + timedelta(days=7)
        }
        orders.append(order)
    return orders

def generate_payments(orders):
    """Generate payment data for paid orders"""
    payments = []
    payment_methods = ["card", "cash", "upi", "bank_transfer"]
    
    paid_orders = [order for order in orders if order["status"] == "paid"]
    
    for i, order in enumerate(paid_orders):
        payment = {
            "payment_id": f"PAY_{i+1:05d}",
            "order_id": order["order_id"],
            "client_id": order["client_id"],
            "amount": order["amount"],
            "payment_date": order["order_date"] + timedelta(days=random.randint(0, 5)),
            "payment_method": random.choice(payment_methods),
            "transaction_id": f"TXN_{uuid.uuid4().hex[:10].upper()}"
        }
        payments.append(payment)
    return payments

def generate_attendance(classes, clients):
    """Generate attendance data"""
    attendance_records = []
    attendance_id = 1
    
    for class_obj in classes:
        if class_obj["status"] == "completed":
            for student_id in class_obj["enrolled_students"]:
                attendance = {
                    "attendance_id": f"ATT_{attendance_id:05d}",
                    "class_id": class_obj["class_id"],
                    "client_id": student_id,
                    "date": class_obj["date"],
                    "attended": random.choice([True, True, True, False]),  # 75% attendance rate
                    "notes": fake.sentence() if random.random() < 0.1 else None
                }
                attendance_records.append(attendance)
                attendance_id += 1
    
    return attendance_records

# Install faker if you don't have it
# pip install faker
